#!/usr/bin/env python3
"""
Script to add sample data for testing the dashboard
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.append('/app')

from app.models import StockMention, StockSentiment, TrendingStock

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/stock_sentiment")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_sample_data():
    db = SessionLocal()
    
    try:
        # Add sample stock mentions
        sample_mentions = [
            StockMention(
                ticker="AAPL",
                text="$AAPL is looking bullish with strong earnings report!",
                sentiment="positive",
                sentiment_score=0.8,
                source="reddit",
                source_id="sample_1"
            ),
            StockMention(
                ticker="AAPL",
                text="Apple stock $AAPL showing great momentum",
                sentiment="positive",
                sentiment_score=0.7,
                source="news",
                source_id="sample_2"
            ),
            StockMention(
                ticker="TSLA",
                text="$TSLA is overvalued and risky",
                sentiment="negative",
                sentiment_score=-0.6,
                source="reddit",
                source_id="sample_3"
            ),
            StockMention(
                ticker="TSLA",
                text="Tesla $TSLA facing production issues",
                sentiment="negative",
                sentiment_score=-0.5,
                source="news",
                source_id="sample_4"
            ),
            StockMention(
                ticker="MSFT",
                text="$MSFT steady performance in cloud computing",
                sentiment="positive",
                sentiment_score=0.4,
                source="reddit",
                source_id="sample_5"
            ),
            StockMention(
                ticker="GOOGL",
                text="Google $GOOGL AI developments look promising",
                sentiment="positive",
                sentiment_score=0.6,
                source="news",
                source_id="sample_6"
            ),
            StockMention(
                ticker="NVDA",
                text="$NVDA GPU demand slowing down",
                sentiment="negative",
                sentiment_score=-0.3,
                source="reddit",
                source_id="sample_7"
            ),
            StockMention(
                ticker="AMZN",
                text="Amazon $AMZN e-commerce growth continues",
                sentiment="positive",
                sentiment_score=0.5,
                source="news",
                source_id="sample_8"
            )
        ]
        
        for mention in sample_mentions:
            db.add(mention)
        
        db.commit()
        print("Added sample mentions")
        
        # Add sample sentiment data for today
        today = datetime.now().date()
        start_date = datetime.combine(today, datetime.min.time())
        
        sample_sentiments = [
            StockSentiment(
                ticker="AAPL",
                date=start_date,
                mentions_count=2,
                positive_mentions=2,
                negative_mentions=0,
                neutral_mentions=0,
                sentiment_index=0.75,
                bullish_score=1.5,
                bearish_score=0.0
            ),
            StockSentiment(
                ticker="TSLA",
                date=start_date,
                mentions_count=2,
                positive_mentions=0,
                negative_mentions=2,
                neutral_mentions=0,
                sentiment_index=-0.55,
                bullish_score=0.0,
                bearish_score=1.1
            ),
            StockSentiment(
                ticker="MSFT",
                date=start_date,
                mentions_count=1,
                positive_mentions=1,
                negative_mentions=0,
                neutral_mentions=0,
                sentiment_index=0.4,
                bullish_score=0.4,
                bearish_score=0.0
            ),
            StockSentiment(
                ticker="GOOGL",
                date=start_date,
                mentions_count=1,
                positive_mentions=1,
                negative_mentions=0,
                neutral_mentions=0,
                sentiment_index=0.6,
                bullish_score=0.6,
                bearish_score=0.0
            ),
            StockSentiment(
                ticker="NVDA",
                date=start_date,
                mentions_count=1,
                positive_mentions=0,
                negative_mentions=1,
                neutral_mentions=0,
                sentiment_index=-0.3,
                bullish_score=0.0,
                bearish_score=0.3
            ),
            StockSentiment(
                ticker="AMZN",
                date=start_date,
                mentions_count=1,
                positive_mentions=1,
                negative_mentions=0,
                neutral_mentions=0,
                sentiment_index=0.5,
                bullish_score=0.5,
                bearish_score=0.0
            )
        ]
        
        for sentiment in sample_sentiments:
            db.add(sentiment)
        
        db.commit()
        print("Added sample sentiment data")
        
        # Add sample trending stocks
        trending_bullish = [
            TrendingStock(
                ticker="AAPL",
                rank=1,
                category="bullish",
                score=1.5,
                mentions_count=2,
                sentiment_index=0.75,
                date=start_date
            ),
            TrendingStock(
                ticker="GOOGL",
                rank=2,
                category="bullish",
                score=0.6,
                mentions_count=1,
                sentiment_index=0.6,
                date=start_date
            ),
            TrendingStock(
                ticker="AMZN",
                rank=3,
                category="bullish",
                score=0.5,
                mentions_count=1,
                sentiment_index=0.5,
                date=start_date
            ),
            TrendingStock(
                ticker="MSFT",
                rank=4,
                category="bullish",
                score=0.4,
                mentions_count=1,
                sentiment_index=0.4,
                date=start_date
            )
        ]
        
        trending_bearish = [
            TrendingStock(
                ticker="TSLA",
                rank=1,
                category="bearish",
                score=1.1,
                mentions_count=2,
                sentiment_index=-0.55,
                date=start_date
            ),
            TrendingStock(
                ticker="NVDA",
                rank=2,
                category="bearish",
                score=0.3,
                mentions_count=1,
                sentiment_index=-0.3,
                date=start_date
            )
        ]
        
        for stock in trending_bullish + trending_bearish:
            db.add(stock)
        
        db.commit()
        print("Added sample trending stocks")
        
        print("Sample data added successfully!")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
