from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging
from typing import List
from datetime import datetime, timedelta
from app.collectors.realtime import RealtimeCollector
from app.collectors.kline import KlineCollector

logger = logging.getLogger(__name__)

class DataCollectionScheduler:
    def __init__(self, symbols: List[str]):
        self.scheduler = AsyncIOScheduler()
        self.symbols = symbols
        
        # 初始化采集器
        self.realtime_collector = RealtimeCollector(symbols)
        self.kline_collector = KlineCollector(symbols)
        
    def start(self):
        """启动调度器"""
        try:
            # 添加实时行情采集任务(每分钟)
            self.scheduler.add_job(
                self.realtime_collector.run,
                trigger=IntervalTrigger(minutes=1),
                id='realtime_collection',
                name='Realtime market data collection'
            )
            
            # 添加日K线采集任务(每天收盘后)
            self.scheduler.add_job(
                self.kline_collector.run,
                trigger=CronTrigger(hour=15, minute=5),  # 15:05执行
                id='daily_kline_collection',
                name='Daily K-line data collection'
            )
            
            # 启动调度器
            self.scheduler.start()
            logger.info("Data collection scheduler started")
            
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            raise
            
    def stop(self):
        """停止调度器"""
        try:
            self.scheduler.shutdown()
            logger.info("Data collection scheduler stopped")
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {str(e)}")
            raise 