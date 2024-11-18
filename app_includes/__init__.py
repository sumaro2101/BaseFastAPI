from .logs_errors import register_errors
from .middlewares import register_middlewares
from .prometheus import register_prometheus


__all__ = ('register_errors',
           'register_middlewares',
           'register_prometheus',
           )
