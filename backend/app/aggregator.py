from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import logging
from .models import StockMention, StockSentiment, TrendingStock

logger = logging.getLogger(__name__)

class SentimentAggregator:
    def __init__(self, db: Session):
        self.db = db
    
    def aggregate_daily_sentiment(self, date: datetime = None) -> List[StockSentiment]:
        """Aggregate daily sentiment data for all stocks"""
        if date is None:
            date = datetime.now().date()
        
        # Get all mentions for the date
        start_date = datetime.combine(date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        
        mentions = self.db.query(StockMention).filter(
            StockMention.created_at >= start_date,
            StockMention.created_at < end_date
        ).all()
        
        # Group by ticker
        ticker_data = {}
        for mention in mentions:
            ticker = mention.ticker
            if ticker not in ticker_data:
                ticker_data[ticker] = {
                    "mentions": [],
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0
                }
            
            ticker_data[ticker]["mentions"].append(mention)
            
            if mention.sentiment == "positive":
                ticker_data[ticker]["positive"] += 1
            elif mention.sentiment == "negative":
                ticker_data[ticker]["negative"] += 1
            else:
                ticker_data[ticker]["neutral"] += 1
        
        # Create StockSentiment records
        sentiment_records = []
        for ticker, data in ticker_data.items():
            total_mentions = len(data["mentions"])
            positive = data["positive"]
            negative = data["negative"]
            neutral = data["neutral"]
            
            # Calculate sentiment index
            if total_mentions > 0:
                sentiment_index = (positive - negative) / total_mentions
            else:
                sentiment_index = 0.0
            
            # Calculate bullish/bearish scores
            # Bullish: high mentions + positive sentiment
            bullish_score = total_mentions * max(0, sentiment_index)
            # Bearish: high mentions + negative sentiment  
            bearish_score = total_mentions * max(0, -sentiment_index)
            
            # Check if record already exists
            existing = self.db.query(StockSentiment).filter(
                StockSentiment.ticker == ticker,
                StockSentiment.date == start_date
            ).first()
            
            if existing:
                # Update existing record
                existing.mentions_count = total_mentions
                existing.positive_mentions = positive
                existing.negative_mentions = negative
                existing.neutral_mentions = neutral
                existing.sentiment_index = sentiment_index
                existing.bullish_score = bullish_score
                existing.bearish_score = bearish_score
                sentiment_records.append(existing)
            else:
                # Create new record
                sentiment_record = StockSentiment(
                    ticker=ticker,
                    date=start_date,
                    mentions_count=total_mentions,
                    positive_mentions=positive,
                    negative_mentions=negative,
                    neutral_mentions=neutral,
                    sentiment_index=sentiment_index,
                    bullish_score=bullish_score,
                    bearish_score=bearish_score
                )
                self.db.add(sentiment_record)
                sentiment_records.append(sentiment_record)
        
        self.db.commit()
        logger.info(f"Aggregated sentiment for {len(sentiment_records)} stocks on {date}")
        
        return sentiment_records
    
    def calculate_trending_stocks(self, date: datetime = None) -> Tuple[List[TrendingStock], List[TrendingStock]]:
        """Calculate trending bullish and bearish stocks"""
        if date is None:
            date = datetime.now().date()
        
        start_date = datetime.combine(date, datetime.min.time())
        
        # Get sentiment data for the date
        sentiment_data = self.db.query(StockSentiment).filter(
            StockSentiment.date == start_date,
            StockSentiment.mentions_count >= 1  # Minimum mentions threshold
        ).all()
        
        # Sort by bullish score for bullish stocks
        bullish_stocks = sorted(
            sentiment_data,
            key=lambda x: x.bullish_score,
            reverse=True
        )[:10]  # Top 10
        
        # Sort by bearish score for bearish stocks
        bearish_stocks = sorted(
            sentiment_data,
            key=lambda x: x.bearish_score,
            reverse=True
        )[:10]  # Top 10
        
        # Create TrendingStock records
        trending_bullish = []
        trending_bearish = []
        
        # Process bullish stocks
        for rank, sentiment in enumerate(bullish_stocks, 1):
            trending_stock = TrendingStock(
                ticker=sentiment.ticker,
                rank=rank,
                category="bullish",
                score=sentiment.bullish_score,
                mentions_count=sentiment.mentions_count,
                sentiment_index=sentiment.sentiment_index,
                date=start_date
            )
            trending_bullish.append(trending_stock)
        
        # Process bearish stocks
        for rank, sentiment in enumerate(bearish_stocks, 1):
            trending_stock = TrendingStock(
                ticker=sentiment.ticker,
                rank=rank,
                category="bearish",
                score=sentiment.bearish_score,
                mentions_count=sentiment.mentions_count,
                sentiment_index=sentiment.sentiment_index,
                date=start_date
            )
            trending_bearish.append(trending_stock)
        
        # Save to database
        for stock in trending_bullish + trending_bearish:
            # Check if record already exists
            existing = self.db.query(TrendingStock).filter(
                TrendingStock.ticker == stock.ticker,
                TrendingStock.category == stock.category,
                TrendingStock.date == start_date
            ).first()
            
            if existing:
                # Update existing record
                existing.rank = stock.rank
                existing.score = stock.score
                existing.mentions_count = stock.mentions_count
                existing.sentiment_index = stock.sentiment_index
            else:
                # Create new record
                self.db.add(stock)
        
        self.db.commit()
        
        logger.info(f"Calculated trending stocks: {len(trending_bullish)} bullish, {len(trending_bearish)} bearish")
        
        return trending_bullish, trending_bearish
    
    def get_historical_sentiment(self, ticker: str, days: int = 7) -> List[StockSentiment]:
        """Get historical sentiment data for a specific ticker"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        return self.db.query(StockSentiment).filter(
            StockSentiment.ticker == ticker,
            StockSentiment.date >= start_date,
            StockSentiment.date <= end_date
        ).order_by(StockSentiment.date.desc()).all()
    
    def get_recent_mentions(self, ticker: str, limit: int = 20) -> List[StockMention]:
        """Get recent mentions for a specific ticker"""
        return self.db.query(StockMention).filter(
            StockMention.ticker == ticker
        ).order_by(StockMention.created_at.desc()).limit(limit).all()
