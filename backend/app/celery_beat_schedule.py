from celery.schedules import crontab

# Celery Beat schedule configuration
beat_schedule = {
    'scrape-reddit-every-30-minutes': {
        'task': 'app.tasks.scrape_reddit_task',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'scrape-news-every-hour': {
        'task': 'app.tasks.scrape_news_task',
        'schedule': crontab(minute=0),  # Every hour at minute 0
    },
    'aggregate-sentiment-every-hour': {
        'task': 'app.tasks.aggregate_sentiment_task',
        'schedule': crontab(minute=15),  # Every hour at minute 15
    },
}

# Timezone
timezone = 'UTC'
