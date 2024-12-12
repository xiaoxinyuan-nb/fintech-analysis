from fastapi import APIRouter
from app.api.v1.market import router as market_router
from app.api.v1.websocket import router as websocket_router

api_router = APIRouter()

@api_router.get("/test")
async def test():
    return {"message": "API router is working"}

# 注册市场数据路由
api_router.include_router(market_router, tags=["market"])
# 注册WebSocket路由
api_router.include_router(websocket_router, tags=["websocket"])