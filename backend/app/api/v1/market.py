from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from app.services.market import market_service
from app.schemas.market import MarketData

router = APIRouter()

@router.get("/market/{symbol}", response_model=MarketData)
async def get_market_data(
    symbol: str,
    include_klines: bool = False,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """获取市场数据"""
    try:
        return await market_service.get_market_data(
            symbol,
            include_klines,
            start_date,
            end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get market data: {str(e)}"
        ) 