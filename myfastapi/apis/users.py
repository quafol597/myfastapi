from fastapi import Depends, HTTPException, Response
from common.router import TimedRoute
from fastapi import APIRouter
from schemas.user_schema import UserInSchema, UserSchema
from models.user_model import Users
from tasks.task_file2 import async_create_user
from configs.logging_settings import logger
from fastapi_limiter.depends import RateLimiter
from fastapi_cache.decorator import cache

router = APIRouter(route_class=TimedRoute)


@router.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))], response_model=list[UserSchema])
async def get_users():
    logger.info("获取用户")
    return await UserSchema.from_queryset(Users.all())


@router.post("/", response_model=UserSchema)
async def create_user(username: UserInSchema):
    user_obj = await Users.create(username=username)
    return await UserSchema.from_tortoise_orm(user_obj)


@cache(expire=10)  # 最好缓存, 入参出参都可以 json 的函数
async def test():
    print("访问到了")
    return "haha"


@router.get("/test_celery")
async def test_celery():
    async_create_user.delay()
    content = await test()
    return Response(content=content)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int):
    return await UserSchema.from_queryset_single(Users.get(id=user_id))


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema):
    await Users.filter(id=user_id).update(**user.model_dump(exclude_unset=True))
    return await UserSchema.from_queryset_single(Users.get(id=user_id))


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Response(message=f"Deleted user {user_id}")
