import logging
import platform
import sys

from useful.logs._json_logging import JSONFormatter

# default JSONFormatter fields
JSON_FIELDS = {
    "message": "message",
    "time": "created",
    "log_level": "levelname",
    "process": "process",
    "process_name": "processName",
    "thread": "thread",
    "thread_name": "threadName",
    "traceback": "exc_text"
}


def setup(logger=None, path=None, log_level=logging.INFO, json_logging=True,
          json_fields=None):
    """
    Setup logging.Logger handlers and formatters. If `json_logging` is set to
    `True`, use custom JSONFormatter, otherwise use regular formatting.
    JSONFormatter supports provides a simple way to write log message, standard
    LogRecord values along with extra keys provided when writing logs.

    Args:
        logger (logging.Logger): A Logger instance to setup. Defaults to None.
        path (str, optional): A path to a file to use for logging. Argument
            supports Formatter with default values for hostname and filename.
            If value is None, use sys.stdout for logging. Defaults to None.
        log_level (int, optional): Set logging level. Defaults to logging.INFO.
        json_logging (boolean, optional): JSON logging format usage indicator.
            Defaults to True.
        json_fields (dict, optional): A dictionary specifying JSONFormatter
            log form. For more details check the documentation of the
            formatter. Defaults to None, which is interpreted as JSON_FIELDS

    Returns:
        logging.Logger: The first argument (logger) after setup.
    """
    json_fields = json_fields or JSON_FIELDS
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
        formatter = JSONFormatter(fields=json_fields,
                                  always_extra={"source": "python"})
    else:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d "
            "(%(process)d): %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
