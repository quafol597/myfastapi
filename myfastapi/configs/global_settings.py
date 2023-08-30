from pydantic_settings import BaseSettings, SettingsConfigDict

# from configs.logging_settings import LOGGING_CONFIG
from pathlib import Path
from configs.tortoise_setting import TORTOISE_ORM
from celery.schedules import crontab


class CeleryConfig(BaseSettings):
    broker_url: str = "redis://42.193.248.250:16379/0"
    result_backend: str = "redis://42.193.248.250:16379/1"
    beat_schedule: dict = {
        "add-every-5-seconds": {"task": "tasks.test2.add", "schedule": 5.0, "args": (16, 16)},
        "add-every-7-seconds": {"task": "tasks.test1.hello", "schedule": 7.0, "args": ()},
    }
    # timezone = "Asia/Shanghai"
    timezone: str = "UTC"
    worker_concurrency: int = 1
    task_default_queue: str = "main_queue"
    # pool: str = "gevent"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_prefix="API__")
    # ===========================初始化配置=================================
    PROJECT_NAME: str = "myfastapi"
    ROOT: str = str(Path(__file__).parent.parent.parent)
    # LOGGING_CONFIG: dict = LOGGING_CONFIG
    LOG_LEVEL: str = "info"
    AUTO_RELOAD: bool = True
    DEBUG: bool = False
    APP_TITLE: str = PROJECT_NAME
    APP_DESCRIPTION: str = "a project template"
    APP_VERSION: str = "v0.1"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    SSE_LOOP_DELAY: int = 1  # sse推送循环延迟时间, second
    SSE_RETRY_TIMEOUT: int = 15000  # sse推送重试时间, milisecond

    # ===========================数据库配置=================================
    MYSQL_URL: str = "mysql://root:123123@42.193.248.250:13306/test_db"
    TORTOISE_ORM: dict = TORTOISE_ORM
    REDIS_URL: str = "redis://42.193.248.250:16379"

    CACHE_REDIS: str = REDIS_URL + "/5"
    LIMIT_REDIS: str = REDIS_URL + "/6"

    # ===========================Celery 配置=================================
    CELERY_CONFIG: CeleryConfig = CeleryConfig()
    # CELERY_BROKER: str = "redis://42.193.248.250:16379/0"
    # ===========================Celery 定时任务配置=================================
    BEAT_SCHEDULE: dict = {}

    # ===========================Middleware 配置=================================
    X_DOMAINS: list = ["*"]
    X_ALLOW_CREDENTIALS: bool = True
    X_METHODS: list = ["*"]
    X_HEADERS: list = [
        "Authorization",
        "Content-Language",
        "Content-Type",
        "Expires",
        "Last-Modified",
        "Accept",
        "Cache-Control",
        "Accept-Encoding",
        "Accept-Language",
        "Debug",
        "BatchJobId",
        "ExpectedJob",
        "Check",
        "x-task-mode",
        "x-channel",
        "x-platform",
        "x-auth-mode",
        "x-osr-version",
        "x-xclient-version",
        "x-console-version",
    ]
    ENFORCE_TRUSTED_HOST: bool = False
    TRUSTED_HOSTS: list = ["*"]
    # responses that smaller than GZIP_MINIMUM_SIZE bytes will not be gziped
    GZIP_MINIMUM_SIZE: int = 500
    ELASTIC_APM_SERVICE_NAME: str | None = None

    # ===========================Email 配置=================================
    MAIL_USERNAME: str = "893180769@qq.com"
    MAIL_PASSWORD: str = "wbhwgvscefiibcbd"
    MAIL_FROM: str = "893180769@qq.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.qq.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False


settings = Settings()
