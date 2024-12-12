import requests
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import time
from app.core.config import settings
from app.core.redis import redis_client

logger = logging.getLogger(__name__)

class FMPClient:
    def __init__(self):
        self.base_url = settings.FMP_API_BASE_URL
        self.api_key = settings.FMP_API_KEY
        self.timeout = settings.FMP_API_TIMEOUT
        self.max_retries = settings.FMP_API_MAX_RETRIES
        
        # 请求会话
        self.session = requests.Session()
        
        # 缓存配置
        self.cache_ttl = {
            'realtime': 60,  # 实时数据缓存1分钟
            'daily': 3600,   # 日K线缓存1小时
            'volume': 300    # 成交量缓存5分钟
        }
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict] = None,
        use_cache: bool = True,
        cache_key: Optional[str] = None,
        cache_ttl: Optional[int] = None
    ) -> Union[Dict, List]:
        """发送API请求并处理响应"""
        
        # 检查缓存
        if use_cache and cache_key:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return cached_data
        
        # 构建请求URL和参数
        url = f"{self.base_url}/{endpoint}"
        params = params or {}
        params['apikey'] = self.api_key
        
        # 重试机制
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                
                # 缓存结果
                if use_cache and cache_key and cache_ttl:
                    redis_client.setex(
                        cache_key,
                        cache_ttl,
                        data
                    )
                
                return data
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # 指数退避
    
    def get_realtime_quote(self, symbol: str) -> Dict:
        """获取实时行情数据"""
        cache_key = f"fmp:realtime:{symbol}"
        
        return self._make_request(
            f"quote/{symbol}",
            use_cache=True,
            cache_key=cache_key,
            cache_ttl=self.cache_ttl['realtime']
        )
    
    def get_daily_kline(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """获取日K线数据"""
        cache_key = f"fmp:daily:{symbol}:{start_date}:{end_date}"
        
        params = {}
        if start_date:
            params['from'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            params['to'] = end_date.strftime('%Y-%m-%d')
            
        return self._make_request(
            f"historical-price-full/{symbol}",
            params=params,
            use_cache=True,
            cache_key=cache_key,
            cache_ttl=self.cache_ttl['daily']
        )
    
    def get_volume_data(self, symbol: str) -> Dict:
        """获取成交量数据"""
        cache_key = f"fmp:volume:{symbol}"
        
        return self._make_request(
            f"historical-price-full/{symbol}",
            params={'serietype': 'volume'},
            use_cache=True,
            cache_key=cache_key,
            cache_ttl=self.cache_ttl['volume']
        )

# 创建全局客户端实例
fmp_client = FMPClient() 