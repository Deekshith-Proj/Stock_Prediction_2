import praw
import os
from typing import List, Dict
import logging
from datetime import datetime, timedelta
from .sentiment_analyzer import FinBERTAnalyzer

logger = logging.getLogger(__name__)

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "StockSentimentBot/1.0")
        )
        self.subreddits = ["stocks", "wallstreetbets", "investing", "SecurityAnalysis"]
        self.analyzer = FinBERTAnalyzer()
    
    def scrape_posts(self, limit: int = 100) -> List[Dict]:
        """Scrape recent posts from finance subreddits"""
        posts_data = []
        
        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get hot posts
                for post in subreddit.hot(limit=limit // len(self.subreddits)):
                    try:
                        # Skip if post is too old (more than 24 hours)
                        post_time = datetime.fromtimestamp(post.created_utc)
                        if post_time < datetime.now() - timedelta(hours=24):
                            continue
                        
                        # Extract stock mentions and analyze sentiment
                        text = f"{post.title} {post.selftext}"
                        mentions = self.analyzer.process_text(text)
                        
                        for mention in mentions:
                            posts_data.append({
                                "ticker": mention["ticker"],
                                "text": mention["text"],
                                "sentiment": mention["sentiment"],
                                "sentiment_score": mention["sentiment_score"],
                                "source": "reddit",
                                "source_id": post.id,
                                "subreddit": subreddit_name,
                                "post_title": post.title,
                                "created_at": post_time
                            })
                    
                    except Exception as e:
                        logger.error(f"Error processing post {post.id}: {e}")
                        continue
            
            except Exception as e:
                logger.error(f"Error scraping subreddit {subreddit_name}: {e}")
                continue
        
        return posts_data
    
    def scrape_comments(self, limit: int = 200) -> List[Dict]:
        """Scrape recent comments from finance subreddits"""
        comments_data = []
        
        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get hot posts and their comments
                for post in subreddit.hot(limit=20):
                    try:
                        post.comments.replace_more(limit=0)  # Get all comments
                        
                        for comment in post.comments.list()[:limit // len(self.subreddits)]:
                            try:
                                # Skip if comment is too old
                                comment_time = datetime.fromtimestamp(comment.created_utc)
                                if comment_time < datetime.now() - timedelta(hours=24):
                                    continue
                                
                                # Skip deleted/removed comments
                                if hasattr(comment, 'body') and comment.body in ['[deleted]', '[removed]']:
                                    continue
                                
                                # Extract stock mentions and analyze sentiment
                                text = comment.body
                                mentions = self.analyzer.process_text(text)
                                
                                for mention in mentions:
                                    comments_data.append({
                                        "ticker": mention["ticker"],
                                        "text": mention["text"],
                                        "sentiment": mention["sentiment"],
                                        "sentiment_score": mention["sentiment_score"],
                                        "source": "reddit",
                                        "source_id": comment.id,
                                        "subreddit": subreddit_name,
                                        "post_title": post.title,
                                        "created_at": comment_time
                                    })
                            
                            except Exception as e:
                                logger.error(f"Error processing comment {comment.id}: {e}")
                                continue
                    
                    except Exception as e:
                        logger.error(f"Error processing post comments {post.id}: {e}")
                        continue
            
            except Exception as e:
                logger.error(f"Error scraping comments from {subreddit_name}: {e}")
                continue
        
        return comments_data
    
    def scrape_all(self) -> List[Dict]:
        """Scrape both posts and comments"""
        all_data = []
        
        logger.info("Starting Reddit scraping...")
        
        # Scrape posts
        posts_data = self.scrape_posts(limit=100)
        all_data.extend(posts_data)
        logger.info(f"Scraped {len(posts_data)} post mentions")
        
        # Scrape comments
        comments_data = self.scrape_comments(limit=200)
        all_data.extend(comments_data)
        logger.info(f"Scraped {len(comments_data)} comment mentions")
        
        logger.info(f"Total Reddit mentions scraped: {len(all_data)}")
        return all_data
