import aiohttp
import time
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class DeribitClient:
    def __init__(self):
        self.url = settings.DERIBIT_API_URL

    async def fetch_index_price(self, currency: str) -> dict:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, params={"index_name": currency}) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return {
                        "ticker": currency,
                        "price": data["result"]["index_price"],
                        "timestamp": int(time.time())
                    }
            except Exception as e:
                logger.error(f"Deribit API error for {currency}: {e}")
                raise