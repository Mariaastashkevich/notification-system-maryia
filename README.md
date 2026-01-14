## Notification System

Python-based notification service that exposes an HTTP API for sending user notifications and delivers them via multiple transport channels (currently **SMS** and **Email**).  
The system persists notifications in PostgreSQL, routes them based on priority, and emits events to an observer-based audit/logging pipeline.

---

### Setup instructions

- **Prerequisites**
  - **Python**: >= 3.10
  - **PostgreSQL**: running instance (local or remote)
  - Recommended: `pyenv` / virtualenv

- **1. Clone and enter the project**

```bash
git clone https://github.com/Mariaastashkevich/notification-system-maryia.git notification-system-maryia
cd notification-system-maryia
```

- **2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

- **3. Install dependencies**

Dependencies are declared in `pyproject.toml`. Install them via:

```bash
pip install -e .
```

If you are not using a build backend that respects `pyproject.toml`, you can alternatively install requirements manually according to the packages used in the codebase (FastAPI, SQLAlchemy, asyncpg/psycopg, pydantic-settings, etc.).

- **4. Configure environment**

1. Copy the example env file:

```bash
cp .env.example .env
```

2. Update the copied file (either `.env` or `.env.example`, see note below) with your own values:
   - **Database**: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME`
   - **Channel toggles & failure rates**: `sms_enabled`, `email_enabled`, `sms_failure_rate`, `email_failure_rate`
   - **Router behaviour**: `channel_priority`

> **Important:**  
> The current configuration classes (`db.config.Settings`, `config.channels.ChannelSettings`, `config.router.RouterSettings`) are set to read from `.env.example`.  
> In a real deployment you would typically point them to `.env` instead; for local development, keeping `.env.example` in sync with your actual `.env` is sufficient.

- **5. Initialize the database**

This project uses Alembic migrations stored under `alembic/`.

```bash
alembic upgrade head
```

Ensure the `DATABASE_URL_*` values derived from your env vars point to the same database on which you run migrations.

- **6. Run the application**

The FastAPI app is exposed via `main.py` as `app`. To run it with Uvicorn:

```bash
uvicorn main:app --reload
```

The notification API will be available (by default) at:

- `POST /notify` — Send a new notification
- `GET /notifications/{notification_id}` — Check status of a previously sent notification

> Compatibility note: the project also exposes `POST /notifications/notify` (same behaviour) because the original router is mounted under the `/notifications` prefix.

You can explore the interactive OpenAPI docs at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

### Design rationale

- **Layered architecture**
  - **API layer (`api/`)**: Defines HTTP endpoints and request/response schemas, and wires dependencies (`api.deps`).
  - **Domain/core layer (`core/`)**: Encapsulates notification concepts like `NotificationMessage`, `NotificationChannel`, `NotificationRouter`, result types, and routing rules.
  - **Infrastructure layer (`channels/`, `db/`, `observer_event_system/`)**: Implements concrete transports (SMS, Email), database access with SQLAlchemy, and event observers for logging/audit.
  - **Configuration layer (`config/`)**: Pydantic-based settings for channels and router behaviour, making the system easily configurable via environment variables.

- **Routing & fallback**
  - The **router** (`core.notification_router.NotificationRouter`) receives a `NotificationMessage` and selects a sequence of channels based on:
    - **Message priority** (e.g. `LOW`, `NORMAL`, `HIGH`, `CRITICAL`).
    - **Configured channel priority** (`config.router.RouterSettings.channel_priority`).
    - **Fallback flag** (`fallback_enabled`) that decides whether to try subsequent channels when one fails.
  - This keeps transport selection and failure-handling logic centralized and testable, while channels remain simple, single-responsibility components.

- **Persistence & auditability**
  - Every notification is persisted first in the `NotificationsOrm` model (`db.models.notification`) with a `PENDING` status.
  - After routing, the `NotificationService` updates the status (`SENT` or `FAILED`), stores the channel used, timestamps, and errors.
  - The **observer/event system** (`observer_event_system/`) emits `NotificationEvent` instances to attached listeners (e.g. `LogListener`, audit trail listeners), enabling:
    - Centralized logging.
    - Extensible hooks (e.g. future metrics, monitoring, or external audit sinks) without coupling them to core business logic.

- **Configuration via environment**
  - All externalized configuration (DB connection, channel toggles, simulated failure rates, router behaviour) is loaded via Pydantic settings classes (`BaseSettings`).
  - This allows for:
    - Consistent behaviour between environments.
    - Safe defaults for local development.
    - Easy override via standard environment variables in production.

---

### API / Transport Layer (justification)

This project exposes its external interface as a **REST API** using **HTTP + JSON** (implemented with **FastAPI**).

#### Why REST (resource-oriented API) for this system

- **Fits the domain model**
  - A notification is a natural **resource**: you create it (`POST /notify`) and then query its state (`GET /notifications/{id}`).
- **Simple integration surface**
  - REST over HTTP is the most widely supported integration style across backend services, web clients, mobile clients, and scripting.
- **Statelessness & scalability**
  - Each request contains everything needed to process it, which makes horizontal scaling straightforward (load balancers, multiple replicas).

#### Why HTTP as the transport protocol

- **Universality**
  - Works everywhere (corporate networks, proxies, cloud LBs), no special clients required.
- **Operational maturity**
  - Mature tooling for observability and operations: logging, tracing, retries at client/gateway, rate limiting, auth, and caching.
- **Good match for request/response workflows**
  - Sending a notification and retrieving its status are naturally request/response operations.

#### Why JSON as the payload format

- **Human-readable & debuggable**
  - Easy to inspect in logs and with tools like `curl`, Postman, Swagger UI.
- **Language-agnostic**
  - Supported out-of-the-box in practically all languages.
- **Adequate performance for this scope**
  - For small notification payloads, JSON overhead is acceptable and the simplicity wins.

#### Why FastAPI specifically

- **Strong typing + validation**
  - Pydantic models validate requests and responses, reducing runtime errors and clarifying the contract.
- **Great developer experience**
  - Automatic OpenAPI docs (`/docs`) and fast iteration speed.
- **Production-friendly**
  - Runs cleanly behind standard ASGI servers (Uvicorn/Gunicorn) and supports async IO patterns.
---

### Transport mechanisms (delivery channels)

The system currently supports two delivery channels:

- **SMS (`SMSChannel`)**
  - Treated as the **primary channel** for most priorities because:
    - SMS is typically the fastest and most attention-grabbing medium.
    - It is well-suited for time-sensitive alerts (e.g. codes, warnings).
  - In the default configuration, **all priorities** route through SMS, with higher priorities additionally failing over to Email when enabled.

- **Email (`EmailChannel`)**
  - Used as a **secondary / fallback channel**, particularly for `HIGH` and `CRITICAL` priorities:
    - Email provides a durable, searchable record of notifications.
    - It is less intrusive than SMS, but still widely accessible.
  - The default routing (`channel_priority`) sends high-importance messages through both SMS and Email to maximize delivery probability and user visibility.

**Why SMS + Email over alternative transports (e.g. push notifications, in-app messages, message queues) for this project:**

- **Simplicity & ubiquity**
  - SMS and Email are universally available and easy to reason about, making them ideal for demonstrating the routing, fallback, and persistence logic without depending on platform-specific push infrastructure.
- **Clear separation of concerns**
  - Both channels implement the same `NotificationChannel` interface, allowing you to introduce additional transports (e.g. push, WhatsApp, webhooks) without altering the router or service logic.
- **Deterministic, testable behaviour**
  - The use of **configurable failure rates** (`sms_failure_rate`, `email_failure_rate`) enables deterministic testing of fallback and error paths for both transports—something that is harder to reliably reproduce with external providers during automated tests.
- **HTTP/JSON as external API transport**
  - The system exposes a **FastAPI-based HTTP JSON API** as the entrypoint. HTTP was chosen because:
    - It is easy to integrate with from virtually any client (mobile, web, backend services).
    - It maps naturally to request/response patterns for “send notification” and “query notification status”.
    - It integrates seamlessly with async workers, gateways, and API management in real-world environments.

Overall, **SMS** provides immediacy, **Email** provides durability, and the **HTTP/JSON API** provides a simple, widely compatible access layer. The router plus observer design make it straightforward to add more transports later without changing the external API.

---

### Environment variables reference (`.env.example`)

The `.env.example` file in the project root contains all configuration keys used by the application. Important variables:

- **Database**
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME` – PostgreSQL connection parameters.
- **Channels**
  - `sms_enabled`, `email_enabled` – enable/disable transports at runtime.
  - `sms_failure_rate`, `email_failure_rate` – simulate provider instability to test routing/fallback.
- **Router**
  - `channel_priority` – JSON string mapping business priority (`LOW`, `NORMAL`, `HIGH`, `CRITICAL`) to an ordered list of channels (`"sms"`, `"email"`).

Use `.env.example` as a template, copy it to `.env`, and adjust the values for your environment.


