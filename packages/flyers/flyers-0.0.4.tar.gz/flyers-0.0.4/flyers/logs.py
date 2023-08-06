import logging
import sys

__LOGGER_FORMAT = '%(asctime)s [%(threadName)s] %(filename)s %(levelname)s: %(message)s'


def get_level():
    return logger.level


def is_debug():
    return logger.level == logging.DEBUG


def set_critical_level():
    logger.setLevel(logging.CRITICAL)


def set_fatal_level():
    logger.setLevel(logging.FATAL)


def set_error_level():
    logger.setLevel(logging.ERROR)


def set_warning_level():
    logger.setLevel(logging.WARNING)


def set_info_level():
    logger.setLevel(logging.INFO)


def set_debug_level():
    logger.setLevel(logging.DEBUG)


def set_notset_level():
    logger.setLevel(logging.NOTSET)


def get_file_logger(name, filename, fmt=__LOGGER_FORMAT, level=logging.INFO):
    handler = logging.FileHandler(filename, encoding='utf-8')
    handler.setFormatter(logging.Formatter(fmt))
    handler.setLevel(level)
    result = logging.getLogger(name)
    result.setLevel(level)
    result.addHandler(handler)
    return result


def get_console_logger(name, stream=sys.stdout, fmt=__LOGGER_FORMAT, level=logging.INFO):
    handler = logging.StreamHandler(stream=stream)
    handler.setFormatter(logging.Formatter(fmt))
    handler.setLevel(level)
    result = logging.getLogger(name)
    result.setLevel(level)
    result.addHandler(handler)
    return result


# default logger
logger = get_console_logger('flyers')
