import logging
import platform
import sys
import threading

from useful.logs._json_logging import JSONFormatter
from useful.logs.exception_hooks import except_logging
from useful.logs.exception_hooks import unraisable_logging
from useful.logs.exception_hooks import threading_except_logging

# default JSONFormatter fields
JSON_FIELDS = {
    "message": "message",
    "time": "created",
    "log_level": "levelname",
    "process": "process",
    "process_name": "processName",
    "thread": "thread",
    "thread_name": "threadName",
    "traceback": "exc_text",
    "__htime": "asctime"
}

ALWAYS_EXTRA = {
   "source": "python"
}


def setup(logger=None, path=None, log_level=logging.INFO, json_logging=True,
          json_fields=None, always_extra=None):
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
        always_extra (dict, optional): A dictionary specifying extra static
             values to always include.

    Returns:
        logging.Logger: The first argument (logger) after setup.
    """
    if json_fields is None:
        json_fields = JSON_FIELDS
    if always_extra is None:
        always_extra = ALWAYS_EXTRA

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
                                  always_extra=always_extra,
                                  datefmt="%Y-%m-%dT%H:%M:%SZ")
    else:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d "
            "(%(process)d): %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # log uncaught exceptions using this logger configuration. This way we can
    # have every important python output in JSON format without the need for
    # multiline parsing afterwards
    sys.excepthook = except_logging
    sys.unraisablehook = unraisable_logging
    # Note: threading.excepthook is only supported since Python 3.8
    if sys.version_info >= (3, 8, 0):
        threading.excepthook = threading_except_logging
    # Note: multiprocessing.Process still doesn't use sys.excepthook, so in
    # order to make it work, you need to implement a custom Process and
    # override Process.run method to make the old stdio output obsolete, catch
    # all exceptions and call sys.excepthook on them
    return logger
