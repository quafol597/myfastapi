"""
项目的管理脚本:
包括启动 api; migrate; upgrade; 启动worker, 启动 celery
"""
import click
from myfastapi.configs import settings
from aerich import Command
import asyncio


@click.group()
def main():
    """默认入口, 什么也不做, 仅提示可用命令"""
    pass


@main.command(context_settings={"ignore_unknown_options": True})
def worker():
    from application import app
    from fastapi.testclient import TestClient
    
    with TestClient(app):
        from tasks.celery import app as celery_app
        celery_app.Worker(loglevel='info').start()
    


@main.command(context_settings={"ignore_unknown_options": True})
def beat():
    from celery.apps.beat import Beat
    from tasks.celery import app
    Beat(app=app, loglevel='info').run()



@main.command(context_settings={"ignore_unknown_options": True})
def initdb():  # 下换线 _ 在命令行中替换成 -
    async def init_db():
        command = Command(tortoise_config=settings.TORTOISE_ORM, app="myfastapi")
        await command.init()
        await command.init_db(safe=True)

    asyncio.run(init_db())


@main.command(context_settings={"ignore_unknown_options": True})
def upgrade():
    async def upgrade():
        command = Command(tortoise_config=settings.TORTOISE_ORM, app="myfastapi")
        await command.init()
        await command.upgrade(run_in_transaction=True)

    asyncio.run(upgrade())


@main.command(context_settings={"ignore_unknown_options": True})
@click.option("-n", "--name", default="update")
def migrate(name):
    async def migrate():
        command = Command(tortoise_config=settings.TORTOISE_ORM, app="myfastapi")
        await command.init()
        await command.migrate(name)

    asyncio.run(migrate())


@main.command(context_settings={"ignore_unknown_options": True})
def api():
    import uvicorn

    uvicorn.run(
        # 传入字符串而不是app的原因是框架要求, 这样开发模式下自动reload才会工作
        "myfastapi.application:app",
        host=settings.HOST,
        port=settings.PORT,
        log_config=settings.LOGGING_CONFIG,
        log_level=settings.LOG_LEVEL,
        debug=settings.DEBUG,
        reload=settings.AUTO_RELOAD,
        reload_dirs=[settings.ROOT],
    )


if __name__ == "__main__":
    main()
