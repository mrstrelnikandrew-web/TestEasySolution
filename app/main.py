import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import router as api_router
from app.db.session import engine
from app.db.models import Base
from sqlalchemy.exc import OperationalError
import asyncio

# Настройка красивого логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_db():
    for i in range(10):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Database tables initialized successfully")
            return
        except (OperationalError, ConnectionRefusedError) as e:
            logger.warning(f"⚠️ Database not ready (attempt {i+1}/10): {e}")
            await asyncio.sleep(2)
    logger.error("❌ Failed to connect to database after 10 attempts")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield
    await engine.dispose()

app = FastAPI(
    title="Deribit Crypto Tracker",
    description="API for tracking BTC and ETH prices from Deribit",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/prices", tags=["Prices"])

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "crypto-tracker-api"}