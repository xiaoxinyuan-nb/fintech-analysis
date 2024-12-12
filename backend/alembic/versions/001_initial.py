"""initial

Revision ID: 001
Revises: 
Create Date: 2024-03-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 创建indices表
    op.create_table(
        'indices',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(32), nullable=False),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('ix_indices_code', 'indices', ['code'])

    # 创建realtime_quotes表
    op.create_table(
        'realtime_quotes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('index_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('change', sa.Float(), nullable=False),
        sa.Column('volume', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['index_id'], ['indices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建kline_data表
    op.create_table(
        'kline_data',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('index_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('open', sa.Float(), nullable=False),
        sa.Column('high', sa.Float(), nullable=False),
        sa.Column('low', sa.Float(), nullable=False),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['index_id'], ['indices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建predictions表
    op.create_table(
        'predictions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('index_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('target_date', sa.DateTime(), nullable=False),
        sa.Column('predicted_price', sa.Float(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['index_id'], ['indices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('predictions')
    op.drop_table('kline_data')
    op.drop_table('realtime_quotes')
    op.drop_index('ix_indices_code', 'indices')
    op.drop_table('indices') 