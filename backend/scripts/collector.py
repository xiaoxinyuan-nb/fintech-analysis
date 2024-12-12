import asyncio
import click
from app.core.config import settings
from app.core.scheduler import DataCollectionScheduler

@click.group()
def cli():
    """数据采集命令行工具"""
    pass

@cli.command()
def start():
    """启动数据采集"""
    scheduler = DataCollectionScheduler(settings.COLLECTION_SYMBOLS)
    scheduler.start()
    
    # 保持程序运行
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()

if __name__ == '__main__':
    cli() 