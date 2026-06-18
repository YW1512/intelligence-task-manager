import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-10s | %(message)s",
    filename="logs/app.log",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def get_custom_logger(name):
    return logging.getLogger(name)