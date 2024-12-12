from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
from app.websockets.manager import manager
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/realtime/{symbol}")
async def realtime_endpoint(websocket: WebSocket, symbol: str):
    """实时行情WebSocket接口"""
    await manager.connect(websocket, "realtime")
    
    try:
        while True:
            # 等待客户端消息
            data = await websocket.receive_text()
            
            # 发送确认消息
            await manager.send_personal_message(
                websocket,
                {
                    "type": "ack",
                    "symbol": symbol,
                    "data": "Message received"
                }
            )
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket, "realtime")
        
@router.websocket("/ws/kline/{symbol}")
async def kline_endpoint(websocket: WebSocket, symbol: str):
    """K线数据WebSocket接口"""
    await manager.connect(websocket, "kline")
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                websocket,
                {
                    "type": "ack",
                    "symbol": symbol,
                    "data": "Message received"
                }
            )
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket, "kline")
        
@router.websocket("/ws/prediction/{symbol}")
async def prediction_endpoint(websocket: WebSocket, symbol: str):
    """预测结果WebSocket接口"""
    await manager.connect(websocket, "prediction")
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                websocket,
                {
                    "type": "ack",
                    "symbol": symbol,
                    "data": "Message received"
                }
            )
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket, "prediction") 