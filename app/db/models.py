from sqlalchemy import BigInteger, String, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TickerPrice(Base):
    __tablename__ = "ticker_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    price: Mapped[float] = mapped_column(Numeric(precision=18, scale=8))
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True)