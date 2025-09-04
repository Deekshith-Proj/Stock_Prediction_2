"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create stock_mentions table
    op.create_table('stock_mentions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(length=10), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('sentiment', sa.String(length=20), nullable=False),
        sa.Column('sentiment_score', sa.Float(), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('source_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('processed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stock_mentions_id'), 'stock_mentions', ['id'], unique=False)
    op.create_index(op.f('ix_stock_mentions_ticker'), 'stock_mentions', ['ticker'], unique=False)

    # Create stock_sentiments table
    op.create_table('stock_sentiments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(length=10), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('mentions_count', sa.Integer(), nullable=True),
        sa.Column('positive_mentions', sa.Integer(), nullable=True),
        sa.Column('negative_mentions', sa.Integer(), nullable=True),
        sa.Column('neutral_mentions', sa.Integer(), nullable=True),
        sa.Column('sentiment_index', sa.Float(), nullable=True),
        sa.Column('bullish_score', sa.Float(), nullable=True),
        sa.Column('bearish_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stock_sentiments_id'), 'stock_sentiments', ['id'], unique=False)
    op.create_index(op.f('ix_stock_sentiments_ticker'), 'stock_sentiments', ['ticker'], unique=False)
    op.create_index(op.f('ix_stock_sentiments_date'), 'stock_sentiments', ['date'], unique=False)

    # Create trending_stocks table
    op.create_table('trending_stocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(length=10), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=20), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('mentions_count', sa.Integer(), nullable=True),
        sa.Column('sentiment_index', sa.Float(), nullable=True),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trending_stocks_id'), 'trending_stocks', ['id'], unique=False)
    op.create_index(op.f('ix_trending_stocks_ticker'), 'trending_stocks', ['ticker'], unique=False)
    op.create_index(op.f('ix_trending_stocks_date'), 'trending_stocks', ['date'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_trending_stocks_date'), table_name='trending_stocks')
    op.drop_index(op.f('ix_trending_stocks_ticker'), table_name='trending_stocks')
    op.drop_index(op.f('ix_trending_stocks_id'), table_name='trending_stocks')
    op.drop_table('trending_stocks')

    op.drop_index(op.f('ix_stock_sentiments_date'), table_name='stock_sentiments')
    op.drop_index(op.f('ix_stock_sentiments_ticker'), table_name='stock_sentiments')
    op.drop_index(op.f('ix_stock_sentiments_id'), table_name='stock_sentiments')
    op.drop_table('stock_sentiments')

    op.drop_index(op.f('ix_stock_mentions_ticker'), table_name='stock_mentions')
    op.drop_index(op.f('ix_stock_mentions_id'), table_name='stock_mentions')
    op.drop_table('stock_mentions')
