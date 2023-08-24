from common.router import router as main_router
from apis.users import router as users_router


main_router.include_router(
    users_router,
    # dependencies=depends_list,
    prefix="/users",
    tags=["Users"],
)
