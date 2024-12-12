import click
from alembic.config import Config
from alembic import command

@click.group()
def cli():
    """数据库迁移命令行工具"""
    pass

@cli.command()
def init():
    """初始化数据库"""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    click.echo("数据库初始化完成")

@cli.command()
def migrate():
    """生成迁移脚本"""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, autogenerate=True)
    click.echo("迁移脚本生成完成")

@cli.command()
def upgrade():
    """升级数据库到最新版本"""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    click.echo("数据库升级完成")

if __name__ == '__main__':
    cli() 