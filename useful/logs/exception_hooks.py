import logging


def except_logging(exc_type, exc_value, exc_traceback):
    """
    Log uncaught exceptions using the root logger. This is a function meant to
    be set as `sys.excepthook` to provide unified logging for regular logs and
    uncaught exceptions.

    Args:
        exc_type (type): Exception type
        exc_value (Exception) : Exception value
        exc_traceback (traceback): Exception traceback
    """
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, exc_traceback))


def threading_except_logging(args):
    """
    Log uncaught exceptions from different threads using the root logger. This
    is a function meant to be set as `threading.excepthook` to provide unified
    logging for regular logs and uncaught exceptions from different threads.

    Note: Only supported since Python version 3.8

    Args:
        args (namedtuple):
            - args.exc_type (type): Exception type
            - args.exc_value (Exception): Exception value, can be None.
                Defaults to None
            - args.exc_traceback (traceback): Exception traceback, can be None.
                Defaults to None
            - args.thread (threading.Thread): Thread which raised the
                exception, can be None. Defaults to None
    """
    exc_type, exc_value, exc_traceback, _ = args
    logging.error("Uncaught threading exception",
                  exc_info=(exc_type, exc_value, exc_traceback))


def unraisable_logging(args):
    """
    Log unraisable exceptions using the root logger. This is a function meant
    to be set as `sys.unraisablehook` to provide unified logging for regular
    logs and unraisable exceptions.

    Args:
        args (namedtuple):
            - args.exc_type (type): Exception type
            - args.exc_value (Exception): Exception value, can be None.
                Defaults to None
            - args.exc_traceback (traceback): Exception traceback, can be None.
                Defaults to None
            - args.err_msg (str): Error message, can be None. Defaults to None
            - args.object (object): Object causing the exception, can be None.
                Defaults to None
    """
    exc_type, exc_value, exc_traceback, err_msg, _ = args
    default_msg = "Unraisable exception"

    logging.error(err_msg or default_msg,
                  exc_info=(exc_type, exc_value, exc_traceback))
