尝试封装了一个 FastAPI 框架. 

目前是: FastAPI + Pydantic + Tortoise + Celery

期望加入: 
    1. Elastic APM 链路追踪.
    2. 错误日志捕获, 可以使用sentry.


docker run -d --rm --name sentry-postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_USER=sentry -v mypostgres:/var/lib/postgresql/data postgres


docker run -it --rm -e SENTRY_SECRET_KEY='7oi^u#p&-l99u5gf%=t359#b0_6i6@@xtbz3*&n32rapht53%3' --link sentry-postgres:postgres --link sentry-redis:redis sentry upgrade

docker run -d --name my-sentry -e SENTRY_SECRET_KEY='7oi^u#p&-l99u5gf%=t359#b0_6i6@@xtbz3*&n32rapht53%3' --link sentry-redis:redis --link sentry-postgres:postgres -p 19000:9000 sentry


docker run -d --name sentry-cron -e SENTRY_SECRET_KEY='7oi^u#p&-l99u5gf%=t359#b0_6i6@@xtbz3*&n32rapht53%3' --link sentry-postgres:postgres --link sentry-redis:redis sentry run cron
docker run -d --name sentry-worker-1 -e SENTRY_SECRET_KEY='7oi^u#p&-l99u5gf%=t359#b0_6i6@@xtbz3*&n32rapht53%3' --link sentry-postgres:postgres --link sentry-redis:redis sentry run worker
