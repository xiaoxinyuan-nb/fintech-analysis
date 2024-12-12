from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Financial Analysis"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered financial data analysis and prediction platform"
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "fintech"
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        case_sensitive = True

settings = Settings() 