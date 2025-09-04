from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import logging

from .database import get_db
from .models import StockMention, StockSentiment, TrendingStock
from .schemas import (
    StockMention as StockMentionSchema,
    StockSentiment as StockSentimentSchema,
    TrendingStock as TrendingStockSchema,
    DashboardResponse,
    StockDetailResponse
)
from .aggregator import SentimentAggregator
from .reddit_scraper import RedditScraper
from .news_scraper import NewsScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock Sentiment API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scrapers
reddit_scraper = RedditScraper()
news_scraper = NewsScraper()

@app.get("/")
async def root():
    return {"message": "Stock Sentiment API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/scrape/reddit")
async def scrape_reddit(db: Session = Depends(get_db)):
    """Scrape Reddit for stock mentions"""
    try:
        mentions_data = reddit_scraper.scrape_all()
        
        # Save to database
        saved_count = 0
        for mention_data in mentions_data:
            try:
                mention = StockMention(
                    ticker=mention_data["ticker"],
                    text=mention_data["text"],
                    sentiment=mention_data["sentiment"],
                    sentiment_score=mention_data["sentiment_score"],
                    source=mention_data["source"],
                    source_id=mention_data["source_id"]
                )
                db.add(mention)
                saved_count += 1
            except Exception as e:
                logger.error(f"Error saving mention: {e}")
                continue
        
        db.commit()
        
        return {
            "message": f"Scraped and saved {saved_count} Reddit mentions",
            "total_found": len(mentions_data)
        }
    
    except Exception as e:
        logger.error(f"Error scraping Reddit: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape/news")
async def scrape_news(db: Session = Depends(get_db)):
    """Scrape news for stock mentions"""
    try:
        mentions_data = news_scraper.scrape_all()
        
        # Save to database
        saved_count = 0
        for mention_data in mentions_data:
            try:
                mention = StockMention(
                    ticker=mention_data["ticker"],
                    text=mention_data["text"],
                    sentiment=mention_data["sentiment"],
                    sentiment_score=mention_data["sentiment_score"],
                    source=mention_data["source"],
                    source_id=mention_data["source_id"]
                )
                db.add(mention)
                saved_count += 1
            except Exception as e:
                logger.error(f"Error saving mention: {e}")
                continue
        
        db.commit()
        
        return {
            "message": f"Scraped and saved {saved_count} news mentions",
            "total_found": len(mentions_data)
        }
    
    except Exception as e:
        logger.error(f"Error scraping news: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/aggregate")
async def aggregate_sentiment(db: Session = Depends(get_db)):
    """Aggregate daily sentiment data"""
    try:
        aggregator = SentimentAggregator(db)
        
        # Aggregate today's sentiment
        sentiment_records = aggregator.aggregate_daily_sentiment()
        
        # Calculate trending stocks
        bullish_stocks, bearish_stocks = aggregator.calculate_trending_stocks()
        
        return {
            "message": "Sentiment aggregation completed",
            "stocks_processed": len(sentiment_records),
            "bullish_stocks": len(bullish_stocks),
            "bearish_stocks": len(bearish_stocks)
        }
    
    except Exception as e:
        logger.error(f"Error aggregating sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard data with top bullish and bearish stocks"""
    try:
        today = datetime.now().date()
        start_date = datetime.combine(today, datetime.min.time())
        
        # Get top 5 bullish stocks
        bullish_stocks = db.query(TrendingStock).filter(
            TrendingStock.category == "bullish",
            TrendingStock.date == start_date
        ).order_by(TrendingStock.rank).limit(5).all()
        
        # Get top 5 bearish stocks
        bearish_stocks = db.query(TrendingStock).filter(
            TrendingStock.category == "bearish",
            TrendingStock.date == start_date
        ).order_by(TrendingStock.rank).limit(5).all()
        
        return DashboardResponse(
            bullish_stocks=bullish_stocks,
            bearish_stocks=bearish_stocks,
            last_updated=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/{ticker}", response_model=StockDetailResponse)
async def get_stock_detail(ticker: str, db: Session = Depends(get_db)):
    """Get detailed information for a specific stock"""
    try:
        ticker = ticker.upper()
        today = datetime.now().date()
        start_date = datetime.combine(today, datetime.min.time())
        
        # Get current sentiment
        current_sentiment = db.query(StockSentiment).filter(
            StockSentiment.ticker == ticker,
            StockSentiment.date == start_date
        ).first()
        
        if not current_sentiment:
            raise HTTPException(status_code=404, detail="Stock not found")
        
        # Get historical sentiment
        aggregator = SentimentAggregator(db)
        historical_sentiment = aggregator.get_historical_sentiment(ticker, days=7)
        
        # Get recent mentions
        recent_mentions = aggregator.get_recent_mentions(ticker, limit=20)
        
        return StockDetailResponse(
            ticker=ticker,
            current_sentiment=current_sentiment,
            historical_sentiment=historical_sentiment,
            recent_mentions=recent_mentions
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stock detail: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sentiment/{ticker}/history")
async def get_sentiment_history(ticker: str, days: int = 7, db: Session = Depends(get_db)):
    """Get sentiment history for a specific stock"""
    try:
        ticker = ticker.upper()
        aggregator = SentimentAggregator(db)
        history = aggregator.get_historical_sentiment(ticker, days)
        
        return {
            "ticker": ticker,
            "history": history,
            "days": days
        }
    
    except Exception as e:
        logger.error(f"Error getting sentiment history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mentions/{ticker}")
async def get_stock_mentions(ticker: str, limit: int = 50, db: Session = Depends(get_db)):
    """Get recent mentions for a specific stock"""
    try:
        ticker = ticker.upper()
        aggregator = SentimentAggregator(db)
        mentions = aggregator.get_recent_mentions(ticker, limit)
        
        return {
            "ticker": ticker,
            "mentions": mentions,
            "count": len(mentions)
        }
    
    except Exception as e:
        logger.error(f"Error getting stock mentions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
