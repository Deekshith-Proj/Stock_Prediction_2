import requests
import os
from typing import List, Dict
import logging
from datetime import datetime, timedelta
from .sentiment_analyzer import FinBERTAnalyzer

logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
        self.headers = {
            "X-API-Key": self.api_key
        }
        self.analyzer = FinBERTAnalyzer()
    
    def search_news(self, query: str, days_back: int = 1) -> List[Dict]:
        """Search for news articles related to the query"""
        if not self.api_key:
            logger.warning("News API key not provided")
            return []
        
        try:
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days_back)
            
            params = {
                "q": query,
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 100
            }
            
            response = requests.get(
                f"{self.base_url}/everything",
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("articles", [])
            else:
                logger.error(f"News API error: {response.status_code} - {response.text}")
                return []
        
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []
    
    def get_finance_news(self) -> List[Dict]:
        """Get general finance news"""
        finance_queries = [
            "stocks market",
            "stock market",
            "trading",
            "investment",
            "earnings",
            "financial news",
            "wall street",
            "nasdaq",
            "dow jones",
            "s&p 500"
        ]
        
        all_articles = []
        
        for query in finance_queries:
            try:
                articles = self.search_news(query, days_back=1)
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Error fetching news for query '{query}': {e}")
                continue
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article.get("url") not in seen_urls:
                seen_urls.add(article["url"])
                unique_articles.append(article)
        
        return unique_articles
    
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """Process articles to extract stock mentions and analyze sentiment"""
        processed_data = []
        
        for article in articles:
            try:
                # Combine title and description
                title = article.get("title", "")
                description = article.get("description", "")
                content = f"{title} {description}"
                
                if not content.strip():
                    continue
                
                # Extract stock mentions and analyze sentiment
                mentions = self.analyzer.process_text(content)
                
                for mention in mentions:
                    processed_data.append({
                        "ticker": mention["ticker"],
                        "text": mention["text"],
                        "sentiment": mention["sentiment"],
                        "sentiment_score": mention["sentiment_score"],
                        "source": "news",
                        "source_id": article.get("url", ""),
                        "article_title": title,
                        "article_url": article.get("url", ""),
                        "published_at": article.get("publishedAt", ""),
                        "created_at": datetime.now()
                    })
            
            except Exception as e:
                logger.error(f"Error processing article: {e}")
                continue
        
        return processed_data
    
    def scrape_all(self) -> List[Dict]:
        """Scrape all news sources"""
        all_data = []
        
        logger.info("Starting news scraping...")
        
        # Get finance news
        articles = self.get_finance_news()
        logger.info(f"Found {len(articles)} news articles")
        
        # Process articles
        processed_data = self.process_articles(articles)
        all_data.extend(processed_data)
        
        logger.info(f"Total news mentions processed: {len(processed_data)}")
        return all_data
