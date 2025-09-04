from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class StockMention(Base):
    __tablename__ = "stock_mentions"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)  # positive, negative, neutral
    sentiment_score = Column(Float, nullable=False)  # -1 to 1
    source = Column(String(50), nullable=False)  # reddit, news
    source_id = Column(String(100), nullable=True)  # reddit post/comment id, news article id
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), server_default=func.now())

class StockSentiment(Base):
    __tablename__ = "stock_sentiments"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    date = Column(DateTime(timezone=True), index=True, nullable=False)
    mentions_count = Column(Integer, default=0)
    positive_mentions = Column(Integer, default=0)
    negative_mentions = Column(Integer, default=0)
    neutral_mentions = Column(Integer, default=0)
    sentiment_index = Column(Float, default=0.0)  # (positive - negative) / total
    bullish_score = Column(Float, default=0.0)  # combined score for ranking
    bearish_score = Column(Float, default=0.0)  # combined score for ranking
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TrendingStock(Base):
    __tablename__ = "trending_stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    rank = Column(Integer, nullable=False)
    category = Column(String(20), nullable=False)  # bullish, bearish
    score = Column(Float, nullable=False)
    mentions_count = Column(Integer, default=0)
    sentiment_index = Column(Float, default=0.0)
    date = Column(DateTime(timezone=True), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
