# useful-logs

A simple function for Python logging setup. Using this allows for the consistent log format across multiple programs, which is very convenient when using microservice architecture. Usage is quite simple, with `useful.logs.setup` requiring only a single call, presumably from the `main` script, for example

```python
import logging
import useful.logs

useful.logs.setup()
_log = logging.getLogger(__name__)


if __name__ == '__main__':
    _log.info("testing", extra={"app": "AppName", "metric": 1.2})
```

Now every other part of the program called from the `main` script uses logging without any
knowledge of log format. An example would be

```python
import logging

_log = logging.getLogger("test")


def test():
    _log.debug("log message", extra={"app": "AppName", "metric": 1.2})
```

When argument `extra` is provided with `JSON` logging enabled, all of the values provided are logged together with timestamps and log message in a `JSON` log.

With this approach you can even have some level of control over log format from other Python modules you do not maintain yourself.
