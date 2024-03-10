import os
import time
import logging

def init_logger(name: str, loglevel, log_dir: str) -> logging.Logger:
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()

    log_path = os.path.join(
        log_dir,
        f"{name}.{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.log",
    )

    logger_file_handler = logging.FileHandler(
        filename=log_path,
        mode='w',
    )
    logger_file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(module)-16s|%(funcName)-32s %(message)s"))

    logger = logging.getLogger(name=name)
    logger.addHandler(logger_file_handler)

    logger.setLevel(loglevel)

    return logger
