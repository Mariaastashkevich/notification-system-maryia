from api.routes.notifications import router as notifications_router
from fastapi import FastAPI, Depends, HTTPException


def create_app() -> FastAPI:
    fastapi_app = FastAPI(title='Notification System')

    fastapi_app.include_router(
        notifications_router,
        prefix='/notifications',
        tags=['notifications'],
    )
    return fastapi_app

