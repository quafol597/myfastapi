import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from main import app
from models import User_Pydantic, Users, UserIn_Pydantic


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url="http://test") as c:
            yield c


@pytest.mark.anyio
async def test_create_user(client: AsyncClient):  # nosec
    response = await client.post("/users", json={"username": "admin", "name": None, "family_name": None})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "admin"
    assert "id" in data
    user_id = data["id"]

    response = await client.get("/user/1")

    print()


if __name__ == "__main__":

    async def haha():
        async with LifespanManager(app) as manager:
            async with AsyncClient(app=manager.app, base_url="http://test") as c:
                return c

    import asyncio

    asyncio.run(haha())
