from pydantic import BaseModel
from datetime import datetime

class PriceResponse(BaseModel):
    ticker: str
    price: float
    timestamp: int

    class Config:
        from_attributes = True