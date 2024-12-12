from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseCollector(ABC):
    """数据采集器基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        
    @abstractmethod
    async def collect(self, **kwargs) -> Any:
        """采集数据"""
        pass
    
    async def process(self, data: Any) -> Any:
        """处理数据"""
        return data
    
    @abstractmethod
    async def save(self, data: Any) -> bool:
        """保存数据"""
        pass
    
    async def run(self, **kwargs) -> bool:
        """运行采集任务"""
        try:
            logger.info(f"Starting {self.name} collection task")
            
            # 采集数据
            data = await self.collect(**kwargs)
            if not data:
                logger.warning(f"{self.name} collected no data")
                return False
                
            # 处理数据
            processed_data = await self.process(data)
            
            # 保存数据
            success = await self.save(processed_data)
            
            if success:
                logger.info(f"{self.name} collection task completed successfully")
            else:
                logger.error(f"{self.name} failed to save data")
                
            return success
            
        except Exception as e:
            logger.error(f"{self.name} collection task failed: {str(e)}")
            return False 