import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_error(client: AsyncClient):
    response = await client.get(
        '/users/get',
    )
    assert response.status_code == 400
