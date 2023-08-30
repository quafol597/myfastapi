import logging
import logging.config
from configs import settings


class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return not settings.DEBUG


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return settings.DEBUG


# 默认的 uvicorn 日志配置在这里: from uvicorn.config import LOGGING_CONFIG
# 下面做一些修改
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            # "fmt": "%(levelprefix)s %(message)s",
            "fmt": "[%(asctime)s] %(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            # "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            "fmt": '[%(asctime)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
        # 自定义 formatters
        "verbose": {"format": "[%(asctime)s] %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s"},
        "simple": {"format": "[%(asctime)s] %(module)s %(lineno)d %(message)s"},
    },
    # 对日志进行过滤
    "filters": {
        "require_debug_false": {
            "()": RequireDebugFalse,
        },
        "require_debug_true": {
            "()": RequireDebugTrue,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        # 自定义两个 handler
        "file": {
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",  # 往文件中写入日志
            "filename": "log.log",
            "maxBytes": 300 * 1024 * 1024,  # 300 MB
            "backupCount": 10,
            "encoding": "utf-8",
            "filters": ["require_debug_false"],
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",  # # 往控制台中写入日志
            "formatter": "simple",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default", "file"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access", "file"], "level": "INFO", "propagate": False},
        "fastapi": {"handlers": ["default", "file"], "level": "DEBUG"},
    },
}

logger = logging.getLogger('fastapi')