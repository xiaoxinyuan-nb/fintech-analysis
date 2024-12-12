from datetime import datetime
from typing import Dict, List
from app.schemas.market import RealtimeQuote, KlineData

def convert_realtime_quote(raw_data: Dict) -> RealtimeQuote:
    """转换实时行情数据格式"""
    return RealtimeQuote(
        symbol=raw_data['symbol'],
        price=raw_data['price'],
        change=raw_data['change'],
        volume=raw_data['volume'],
        timestamp=datetime.fromtimestamp(raw_data['timestamp'])
    )

def convert_kline_data(raw_data: Dict) -> KlineData:
    """转换K线数据格式"""
    return KlineData(
        date=datetime.strptime(raw_data['date'], '%Y-%m-%d'),
        open=raw_data['open'],
        high=raw_data['high'],
        low=raw_data['low'],
        close=raw_data['close'],
        volume=raw_data['volume']
    ) 