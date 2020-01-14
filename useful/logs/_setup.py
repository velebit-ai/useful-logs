import logging
import platform
import sys

from pythonjsonlogger import jsonlogger

# Default json logging values. Everything except message is set automatically
SUPPORTED_KEYS = [
    'asctime',
    'created',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'thread',
    'threadName'
]


def _log_format(x):
    """
    Take an iterable of strings and convert them into a logging formatter
    compatible format: %(variable_name)

    Args:
        x ([str]): An iterable of strings to format

    Returns:
        [str]: A list of formatted strings
    """
    return ['%({})'.format(i) for i in x]


class AddSrcJsonFormatter(jsonlogger.JsonFormatter):
    """
    A custom JsonFormatter implementation that adds {"src": "python"} to
    JSON log.
    """
    def add_fields(self, log_record, record, message_dict):
        super(AddSrcJsonFormatter, self).add_fields(log_record, record, message_dict)
        # add {"src": "python"} to log record
        log_record["src"] = "python"


def setup(logger=None, path=None, log_level=logging.INFO, json_logging=True,
          supported_keys=None):
    """
    Setup logging.Logger handlers and formatters. If `json_logging` is set to
    `True`, use json formatting per single message, otherwise use regular
    formatting.

    If `json_logging=True`, when running `logger.info(msg, extra={...})`, `msg`
    is parsed as key `"message"`, and everything in dict provided as `extra` is
    added to the final log. This provides a simple way to add custom metrics to
    logs.

    Note:
        The important thing to notice is that every key from supported_keys
        (or SUPPORTED_KEYS as default) except `"message"` is filled
        automatically, and these keys **must** not be overriden in `extra`.
        When calling

            `logger.info("testing", extra={"app": "AppName", "metric": 1.2})`

        we get a json in form of:

                    {
                        "asctime": "2019-08-22 11:09:33,805",
                        "created": 1566464973.8052688,
                        "filename": "main.py",
                        "funcName": "<module>",
                        "levelname": "INFO",
                        "levelno": 20,
                        "lineno": 8,
                        "module": "main",
                        "msecs": 805.2687644958496,
                        "message": "testing",
                        "name": "root",
                        "pathname": "/path/to/main.py",
                        "process": 32621,
                        "processName": "MainProcess",
                        "relativeCreated": 35.19701957702637,
                        "thread": 139825143863104,
                        "threadName": "MainThread",
                        "app": "AppName",
                        "metric": 1.2
                    }

    Args:
        logger (logging.Logger): A Logger instance to setup. Defaults to None.
        path (str, optional): A path to a file to use for logging. Argument
            supports Formatter with default values for hostname and filename.
            If value is None, use sys.stdout for logging. Defaults to None.
        log_level (int, optional): Set logging level. Defaults to logging.INFO.
        json_logging (boolean, optional): JSON logging format usage indicator.
            Defaults to True.
        supported_keys (list, optional): set json logging supported keys.
            Defaults to None, which uses SUPPORTED_KEYS.

    Returns:
        logging.Logger: The first argument (logger) after setup.
    """
    supported_keys = supported_keys or SUPPORTED_KEYS
    if logger is None:
        logger = logging.getLogger()

    logger.setLevel(log_level)

    if path is None:
        handler = logging.StreamHandler(sys.stdout)
    else:
        # replace {hostname} and {filename} in path
        path = path.format(hostname=platform.node(), filename="python.log")
        handler = logging.FileHandler(path)

    if json_logging:
        custom_format = ' '.join(_log_format(supported_keys))
        formatter = AddSrcJsonFormatter(custom_format)
    else:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d "
            "(%(process)d): %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
