from functools import wraps

from pytemplate.domain.models import LogLevel


def validate_log_level(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'level' in kwargs:
            level = kwargs["level"]
            if not isinstance(level, LogLevel):
                raise TypeError(f"Level argument must be of type LogLevel, not {type(level)}")
            kwargs["level"] = level.value
        return func(*args, **kwargs)

    return wrapper
