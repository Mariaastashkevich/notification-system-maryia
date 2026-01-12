import logging


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)d %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )