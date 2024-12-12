from typing import Dict, List
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from app.collectors.base import BaseCollector
from app.clients.fmp import fmp_client
from app.models.quotes import RealtimeQuote
from app.core.database import get_db
from app.utils.converter import convert_realtime_quote
from app.services.push import push_service

logger = logging.getLogger(__name__)

class RealtimeCollector(BaseCollector):
    """实时行情数据采集器"""
    
    def __init__(self, symbols: List[str]):
        super().__init__()
        self.symbols = symbols
        
    async def collect(self, **kwargs) -> List[Dict]:
        """采集实时行情数据"""
        results = []
        for symbol in self.symbols:
            try:
                data = fmp_client.get_realtime_quote(symbol)
                results.append(data)
            except Exception as e:
                logger.error(f"Failed to collect realtime data for {symbol}: {str(e)}")
                continue
        return results
    
    async def process(self, data: List[Dict]) -> List[RealtimeQuote]:
        """处理实时行情数据"""
        return [convert_realtime_quote(item) for item in data]
    
    async def save(self, quotes: List[RealtimeQuote]) -> bool:
        """保存实时行情数据"""
        try:
            db = next(get_db())
            for quote in quotes:
                db_quote = RealtimeQuote(
                    symbol=quote.symbol,
                    price=quote.price,
                    change=quote.change,
                    volume=quote.volume,
                    timestamp=quote.timestamp
                )
                db.add(db_quote)
            db.commit()
            
            # 推送数据
            for quote in quotes:
                await push_service.push_realtime_quote(
                    quote.symbol,
                    quote.dict()
                )
            
            return True
        except Exception as e:
            logger.error(f"Failed to save realtime quotes: {str(e)}")
            return False 