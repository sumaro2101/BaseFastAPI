import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_error(client: AsyncClient, user_test_data):
    response = await client.post(
        '/auth/register',
        json=user_test_data,
    )
    assert response.status_code == 201
