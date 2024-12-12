from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class RealtimeQuote(BaseModel):
    symbol: str
    price: float
    change: float
    volume: float
    timestamp: datetime

class KlineData(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class MarketData(BaseModel):
    symbol: str
    realtime: Optional[RealtimeQuote]
    klines: Optional[List[KlineData]] 