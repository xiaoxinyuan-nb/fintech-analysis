from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session
from app.collectors.base import BaseCollector
from app.clients.fmp import fmp_client
from app.models.quotes import KlineData
from app.core.database import get_db
from app.utils.converter import convert_kline_data

logger = logging.getLogger(__name__)

class KlineCollector(BaseCollector):
    """K线数据采集器"""
    
    def __init__(self, symbols: List[str]):
        super().__init__()
        self.symbols = symbols
        
    async def collect(self, **kwargs) -> Dict[str, List[Dict]]:
        """采集K线数据"""
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        
        results = {}
        for symbol in self.symbols:
            try:
                data = fmp_client.get_daily_kline(
                    symbol,
                    start_date,
                    end_date
                )
                results[symbol] = data
            except Exception as e:
                logger.error(f"Failed to collect kline data for {symbol}: {str(e)}")
                continue
        return results
    
    async def process(self, data: Dict[str, List[Dict]]) -> List[KlineData]:
        """处理K线数据"""
        processed = []
        for symbol, klines in data.items():
            for kline in klines:
                processed.append(convert_kline_data(kline))
        return processed
    
    async def save(self, klines: List[KlineData]) -> bool:
        """保存K线数据"""
        try:
            db = next(get_db())
            for kline in klines:
                db_kline = KlineData(
                    date=kline.date,
                    open=kline.open,
                    high=kline.high,
                    low=kline.low,
                    close=kline.close,
                    volume=kline.volume
                )
                db.add(db_kline)
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save kline data: {str(e)}")
            return False 