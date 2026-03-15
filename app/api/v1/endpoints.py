# app/api/v1/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from app.db.session import get_db
from app.db.models import TickerPrice
from app.schemas.price import PriceResponse

router = APIRouter()

@router.get("/all", response_model=List[PriceResponse])
async def get_all_prices(
    ticker: str = Query(..., example="btc_usd"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(TickerPrice).where(TickerPrice.ticker == ticker).order_by(TickerPrice.timestamp)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/last", response_model=PriceResponse)
async def get_last_price(
    ticker: str = Query(..., example="btc_usd"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(TickerPrice).where(TickerPrice.ticker == ticker).order_by(desc(TickerPrice.timestamp))
    result = await db.execute(stmt)
    price = result.scalars().first()
    if not price:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return price

@router.get("/filter", response_model=List[PriceResponse])
async def get_prices_by_date(
    ticker: str = Query(...),
    start_ts: int = Query(...),
    end_ts: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(TickerPrice).where(
        TickerPrice.ticker == ticker,
        TickerPrice.timestamp.between(start_ts, end_ts)
    )
    result = await db.execute(stmt)
    return result.scalars().all()