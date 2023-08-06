import logging
from collections import defaultdict
_LOGGERS: defaultdict = defaultdict()


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    return logger


def get_logger(name: str = '__root__') -> logging.Logger:
    logger = _LOGGERS.get(name)
    if not logger:
        logger = create_logger(name)
        _LOGGERS[name] = logger
    return logger
