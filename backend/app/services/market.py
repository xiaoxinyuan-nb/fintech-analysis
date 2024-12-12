from typing import Dict, List, Optional
from datetime import datetime
import logging
from app.clients.fmp import fmp_client
from app.utils.converter import convert_realtime_quote, convert_kline_data
from app.schemas.market import MarketData, RealtimeQuote, KlineData

logger = logging.getLogger(__name__)

class MarketDataService:
    @staticmethod
    async def get_market_data(
        symbol: str,
        include_klines: bool = False,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> MarketData:
        """获取市场数据"""
        try:
            # 获取实时行情
            realtime_data = fmp_client.get_realtime_quote(symbol)
            realtime_quote = convert_realtime_quote(realtime_data)
            
            # 获取K线数据
            klines = None
            if include_klines:
                raw_klines = fmp_client.get_daily_kline(
                    symbol,
                    start_date,
                    end_date
                )
                klines = [convert_kline_data(k) for k in raw_klines]
            
            return MarketData(
                symbol=symbol,
                realtime=realtime_quote,
                klines=klines
            )
            
        except Exception as e:
            logger.error(f"Failed to get market data for {symbol}: {str(e)}")
            raise

market_service = MarketDataService() 