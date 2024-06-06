from functools import wraps

from pytemplate.domain.models import LogLevel


def validate_log_level(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(level, LogLevel):
                raise TypeError(f"Level argument must be of type LogLevel, not {type(level)}")
            if level.value not in [log.value for log in LogLevel]:
                raise ValueError(f"Invalid LogLevel value: {level.value}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
