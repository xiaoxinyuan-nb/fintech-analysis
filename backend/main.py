from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.app.core.config import settings
from backend.app.api.v1.router import api_router

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 临时允许所有源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to AI Financial Analysis API"} 