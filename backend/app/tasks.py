from celery import current_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import logging
from datetime import datetime

from .celery_app import celery_app
from .database import SessionLocal
from .reddit_scraper import RedditScraper
from .news_scraper import NewsScraper
from .aggregator import SentimentAggregator
from .models import StockMention

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def scrape_reddit_task(self):
    """Celery task to scrape Reddit data"""
    try:
        logger.info("Starting Reddit scraping task")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "Scraping Reddit..."})
        
        # Initialize scraper
        reddit_scraper = RedditScraper()
        
        # Scrape data
        mentions_data = reddit_scraper.scrape_all()
        
        # Save to database
        db = SessionLocal()
        saved_count = 0
        
        try:
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
            logger.info(f"Saved {saved_count} Reddit mentions")
            
            return {
                "status": "completed",
                "saved_count": saved_count,
                "total_found": len(mentions_data)
            }
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Error in Reddit scraping task: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def scrape_news_task(self):
    """Celery task to scrape news data"""
    try:
        logger.info("Starting news scraping task")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "Scraping news..."})
        
        # Initialize scraper
        news_scraper = NewsScraper()
        
        # Scrape data
        mentions_data = news_scraper.scrape_all()
        
        # Save to database
        db = SessionLocal()
        saved_count = 0
        
        try:
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
            logger.info(f"Saved {saved_count} news mentions")
            
            return {
                "status": "completed",
                "saved_count": saved_count,
                "total_found": len(mentions_data)
            }
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Error in news scraping task: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def aggregate_sentiment_task(self):
    """Celery task to aggregate sentiment data"""
    try:
        logger.info("Starting sentiment aggregation task")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "Aggregating sentiment..."})
        
        # Initialize aggregator
        db = SessionLocal()
        aggregator = SentimentAggregator(db)
        
        try:
            # Aggregate today's sentiment
            sentiment_records = aggregator.aggregate_daily_sentiment()
            
            # Calculate trending stocks
            bullish_stocks, bearish_stocks = aggregator.calculate_trending_stocks()
            
            logger.info(f"Aggregated sentiment for {len(sentiment_records)} stocks")
            
            return {
                "status": "completed",
                "stocks_processed": len(sentiment_records),
                "bullish_stocks": len(bullish_stocks),
                "bearish_stocks": len(bearish_stocks)
            }
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Error in sentiment aggregation task: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def full_scraping_task(self):
    """Full scraping task that runs all scrapers and aggregates data"""
    try:
        logger.info("Starting full scraping task")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "Starting full scraping..."})
        
        # Run Reddit scraping
        reddit_result = scrape_reddit_task.delay()
        reddit_result.get(timeout=1800)  # 30 minutes timeout
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "Reddit scraping completed, scraping news..."})
        
        # Run news scraping
        news_result = scrape_news_task.delay()
        news_result.get(timeout=1800)  # 30 minutes timeout
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "News scraping completed, aggregating sentiment..."})
        
        # Aggregate sentiment
        aggregate_result = aggregate_sentiment_task.delay()
        aggregate_result.get(timeout=600)  # 10 minutes timeout
        
        logger.info("Full scraping task completed successfully")
        
        return {
            "status": "completed",
            "reddit_result": reddit_result.result,
            "news_result": news_result.result,
            "aggregate_result": aggregate_result.result
        }
    
    except Exception as e:
        logger.error(f"Error in full scraping task: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise
