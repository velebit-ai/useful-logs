import json
import logging

from useful.logs._context import context

# a set of standard LogRecord attributes to be used when building JSON logs
LOG_RECORD_ATTRIBUTES = {
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs', 'message',
    'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated',
    'stack_info', 'thread', 'threadName'}


class JSONFormatter(logging.Formatter):
    """
    Simple logging formatter using JSON serialization.
    """
    def __init__(self, fields=None, always_extra=None, datefmt=None):
        """
        Args:
            fields (dict, optional): A dictionary of fields to use in the log.
                The keys in the dictionary are keys that will be used in the
                final log form, and its values are the names of the attributes
                from the log record to use as final log values. Defaults to
                None, which is interpreted as an empty dict.
            always_extra (dict, optional): A dictionary of additional static
                values written to the final log. Defaults to None, which is
                interpreted as an empty dict.
            datefmt (str, optional): strftime date format. For more details
                check logging.Formatter documentation. Defaults to None.
        """
        super().__init__(fmt=None, datefmt=datefmt, style='%')
        self.fields = fields or {}
        self._uses_time = "asctime" in self.fields.values()
        self.always_extra = always_extra or {}

    def usesTime(self):
        """
        Check if the format uses the creation time of the record. For more
        information about the method see logging.Formatter.
        """
        return self._uses_time

    def format(self, record):
        """
        Build a JSON serializable dict starting from `self.always_extra`,
        adding the data from the LogRecord specified in `self.fields`, and
        finally adding the record specific extra data.

        Args:
            record (logging.LogRecord): log record to be converted to string

        Returns:
            string: JSON serialized log record
        """
        # start with always_extra data to prevent overriding log record data
        data = self.always_extra.copy()

        # format non-serializable record values. For more details see method
        # logging.Formatter.format()
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        record.stack_info = self.formatStack(record.stack_info)

        # extract wanted fields from log record
        for key, field in self.fields.items():
            value = record.__dict__.get(field, None)

            # use cached exception traceback
            if field == "exc_info":
                value = record.exc_text

            # skip record fields without data
            if value:
                data[key] = value

        # copy only LogRecord extra
        for field, value in record.__dict__.items():
            # skip all standard fields
            if field in LOG_RECORD_ATTRIBUTES:
                continue
            # skip all internal variables and names
            if field.startswith("_"):
                continue

            data[field] = value

        # add the data from useful.logs.context
        data = {**data, **context.__dict__}

        return json.dumps(data)
