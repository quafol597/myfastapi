import time

from fastapi.staticfiles import StaticFiles
from configs import settings
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from elasticapm.contrib.starlette import make_apm_client
from elasticapm.instrumentation.register import register as register_to_elasticapm


class App(FastAPI):
    def __init__(self, **kwargs):
        self.start_time = time.time()

        super(App, self).__init__(
            debug=settings.DEBUG,
            title=settings.APP_TITLE,
            description=settings.APP_DESCRIPTION,
            version=settings.APP_VERSION,
            **kwargs,
        )
        self.load_router()
        self.load_models()
        self.load_sentry()
        self.setup_middlewares()
        self.mount("/static", StaticFiles(directory=f"{settings.ROOT}/static"), name="static")

    def load_models(self):
        register_tortoise(
            self,
            config=settings.TORTOISE_ORM,
            add_exception_handlers=True,
        )
    def load_sentry(self):
        import sentry_sdk
        sentry_sdk.init("http://5b9dc94e89e5431086f997a0ddb48355@42.193.248.250:19000/2")

    def load_router(self):
        from apis import main_router

        self.include_router(main_router)

    def setup_middlewares(self) -> None:
        self.add_middleware(
            CORSMiddleware,
            allow_origins=settings.X_DOMAINS,
            allow_credentials=settings.X_ALLOW_CREDENTIALS,
            allow_methods=settings.X_METHODS,
            allow_headers=settings.X_HEADERS,
        ),
        self.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MINIMUM_SIZE)

        if settings.ENFORCE_TRUSTED_HOST:
            self.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)

        if settings.ELASTIC_APM_SERVICE_NAME:
            # make_apm_client 会注入环境变量中 ELASTIC_APM_* 的合法值,但是从config中传入的话参数需要处理，为了保持一致， 人工注入
            from elasticapm.instrumentation.register import register
            from elasticapm.contrib.starlette import ElasticAPM
            from elasticapm.conf import Config as APMConfig

            register("bello_vangogh.elasticapm.instrumentation.packages.mongodb.VanGoghMongoInstrumentation")
            apm_config = APMConfig(env_dict=settings)
            apm = make_apm_client(apm_config.values)
            self.add_middleware(ElasticAPM, client=apm)


app = App()
