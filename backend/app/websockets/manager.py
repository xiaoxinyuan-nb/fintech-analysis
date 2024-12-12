import logging
from typing import Dict, Set
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # 活跃连接
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "realtime": set(),  # 实时行情订阅者
            "kline": set(),     # K线数据订阅者
            "prediction": set() # 预测结果订阅者
        }
        
    async def connect(self, websocket: WebSocket, channel: str):
        """建立连接"""
        await websocket.accept()
        if channel in self.active_connections:
            self.active_connections[channel].add(websocket)
            logger.info(f"Client connected to {channel} channel")
        
    async def disconnect(self, websocket: WebSocket, channel: str):
        """断开连接"""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
            logger.info(f"Client disconnected from {channel} channel")
        
    async def broadcast(self, channel: str, message: dict):
        """广播消息"""
        if channel not in self.active_connections:
            return
            
        # 添加时间戳
        message["timestamp"] = datetime.utcnow().isoformat()
        
        # 序列化消息
        data = json.dumps(message)
        
        # 广播给所有订阅者
        for connection in self.active_connections[channel]:
            try:
                await connection.send_text(data)
            except Exception as e:
                logger.error(f"Failed to send message: {str(e)}")
                await self.disconnect(connection, channel)
                
    async def send_personal_message(self, websocket: WebSocket, message: dict):
        """发送个人消息"""
        try:
            # 添加时间戳
            message["timestamp"] = datetime.utcnow().isoformat()
            
            # 序列化消息
            data = json.dumps(message)
            
            await websocket.send_text(data)
        except Exception as e:
            logger.error(f"Failed to send personal message: {str(e)}")

# 创建全局连接管理器实例
manager = ConnectionManager() 