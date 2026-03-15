import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_get_last_price_not_found():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Передаем параметры правильно через params
        response = await ac.get("/prices/last", params={"ticker": "unknown_coin"})

    assert response.status_code == 404
    assert "detail" in response.json()