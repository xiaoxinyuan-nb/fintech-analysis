"""seed initial data

Revision ID: 002
Revises: 001
Create Date: 2024-03-20 10:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # 添加三大指数的初始数据
    op.execute(
        """
        INSERT INTO indices (id, code, name, description)
        VALUES 
        (
            '{}', 
            'SSE', 
            '上证指数', 
            'SSE Composite Index'
        ),
        (
            '{}',
            'SZSE',
            '深证成指',
            'SZSE Component Index'
        ),
        (
            '{}',
            'ChiNext',
            '创业板指',
            'ChiNext Index'
        );
        """.format(
            uuid.uuid4(),
            uuid.uuid4(),
            uuid.uuid4()
        )
    )

def downgrade():
    op.execute("DELETE FROM indices WHERE code IN ('SSE', 'SZSE', 'ChiNext');") 