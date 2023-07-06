import logging
from fastapi.logger import logger
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler('app/logfile.log', maxBytes=10000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_error_logger = logging.getLogger("uvicorn.error")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

logger.handlers = gunicorn_error_logger.handlers
gunicorn_error_logger.addHandler(file_handler)
gunicorn_logger.addHandler(file_handler)
uvicorn_access_logger.addHandler(file_handler)

if __name__ != "__main__":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)
