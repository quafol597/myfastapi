from schemas.user_schema import UserSchema
from .celery import app
from common.task_decorator import task_decorator
from asgiref.sync import async_to_sync
from models.user_model import Users
import time
import asyncio


@app.task
def add(x, y):
    return x + y


@app.task
@task_decorator
async def async_create_user():
    user_obj = await Users.create(username=f"haha_{int(time.time())}")
    return UserSchema.model_validate(user_obj).model_dump()


# @app.task
# def async_create_user():
#     return asyncio.run(async_create_user2())
