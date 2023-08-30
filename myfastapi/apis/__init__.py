from common.router import router as main_router
from apis.users import router as users_router
from apis.tests import router as tests_router


main_router.include_router(users_router, prefix="/users", tags=["Users"])
main_router.include_router(tests_router, prefix="/tests", tags=["tests"])
