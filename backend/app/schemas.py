from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class StockMentionBase(BaseModel):
    ticker: str
    text: str
    sentiment: str
    sentiment_score: float
    source: str
    source_id: Optional[str] = None

class StockMentionCreate(StockMentionBase):
    pass

class StockMention(StockMentionBase):
    id: int
    created_at: datetime
    processed_at: datetime

    class Config:
        from_attributes = True

class StockSentimentBase(BaseModel):
    ticker: str
    date: datetime
    mentions_count: int
    positive_mentions: int
    negative_mentions: int
    neutral_mentions: int
    sentiment_index: float
    bullish_score: float
    bearish_score: float

class StockSentimentCreate(StockSentimentBase):
    pass

class StockSentiment(StockSentimentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TrendingStockBase(BaseModel):
    ticker: str
    rank: int
    category: str
    score: float
    mentions_count: int
    sentiment_index: float
    date: datetime

class TrendingStockCreate(TrendingStockBase):
    pass

class TrendingStock(TrendingStockBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    bullish_stocks: List[TrendingStock]
    bearish_stocks: List[TrendingStock]
    last_updated: datetime

class StockDetailResponse(BaseModel):
    ticker: str
    current_sentiment: StockSentiment
    historical_sentiment: List[StockSentiment]
    recent_mentions: List[StockMention]
