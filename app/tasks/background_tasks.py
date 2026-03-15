import asyncio
import logging
from app.celery_app import celery_app
from app.services.deribit_client import DeribitClient
from app.db.models import TickerPrice
from app.db.session import async_session

logger = logging.getLogger(__name__)

async def run_fetch_prices():
    client = DeribitClient()
    tickers = ["btc_usd", "eth_usd"]

    async with async_session() as session:
        for ticker in tickers:
            try:
                data = await client.fetch_index_price(ticker)
                session.add(TickerPrice(**data))
                logger.info(f"Fetched {ticker}: {data['price']}")
            except Exception as e:
                logger.error(f"Failed task for {ticker}: {e}")

        await session.commit()


@celery_app.task(name="app.tasks.background_tasks.fetch_prices_task")
def fetch_prices_task():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(run_fetch_prices())