import logging
import asyncio
from typing import Dict, Any
from app.websockets.manager import manager
from app.core.config import settings

logger = logging.getLogger(__name__)

class DataPushService:
    @staticmethod
    async def push_realtime_quote(symbol: str, data: Dict[str, Any]):
        """推送实时行情数据"""
        try:
            await manager.broadcast(
                "realtime",
                {
                    "type": "realtime",
                    "symbol": symbol,
                    "data": data
                }
            )
        except Exception as e:
            logger.error(f"Failed to push realtime quote: {str(e)}")
            
    @staticmethod
    async def push_kline_update(symbol: str, data: Dict[str, Any]):
        """推送K线数据更新"""
        try:
            await manager.broadcast(
                "kline",
                {
                    "type": "kline",
                    "symbol": symbol,
                    "data": data
                }
            )
        except Exception as e:
            logger.error(f"Failed to push kline update: {str(e)}")
            
    @staticmethod
    async def push_prediction(symbol: str, data: Dict[str, Any]):
        """推送预测结果"""
        try:
            await manager.broadcast(
                "prediction",
                {
                    "type": "prediction",
                    "symbol": symbol,
                    "data": data
                }
            )
        except Exception as e:
            logger.error(f"Failed to push prediction: {str(e)}")

# 创建全局推送服务实例
push_service = DataPushService() 