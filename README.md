# Stock Sentiment Recommender

An AI-powered stock sentiment analysis platform that aggregates real-time data from Reddit and news sources to provide live sentiment insights and stock recommendations.

## Features

- 🔍 **Real-time Data Collection**: Live scraping from Reddit (r/stocks, r/wallstreetbets, r/investing, r/SecurityAnalysis) and financial news
- 🤖 **AI Sentiment Analysis**: Uses FinBERT for accurate financial sentiment analysis with lazy loading
- 📊 **Interactive Dashboard**: Beautiful charts and visualizations with Recharts showing live data
- 📈 **Live Stock Rankings**: Real-time bullish/bearish stock rankings based on current sentiment
- 🔄 **Automated Processing**: Celery-based task scheduling with configurable intervals
- 🐳 **Docker Ready**: Complete containerized setup with health checks and proper networking
- ⚡ **Live Updates**: Dashboard refreshes automatically with new data every 30 minutes

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Reliable relational database
- **Celery + Redis** - Task queue and caching
- **FinBERT** - Financial sentiment analysis model
- **PRAW** - Reddit API wrapper
- **News API** - Financial news aggregation

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Lucide React** - Beautiful icons

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Reddit API credentials
- News API key

### 1. Clone and Setup

```bash
git clone https://github.com/Deekshith-Proj/Stock_Prediction_2
cd stock_pred_2
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Reddit API (Get from https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# News API (Get from https://newsapi.org/)
NEWS_API_KEY=your_news_api_key
```

### 3. Start the Application

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head
```

### 5. Access the Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 6. Get Real-Time Data

```bash
# Scrape Reddit data (manual trigger)
Invoke-WebRequest -Uri "http://localhost:8000/scrape/reddit" -Method POST

# Scrape news data (manual trigger)
Invoke-WebRequest -Uri "http://localhost:8000/scrape/news" -Method POST

# Aggregate sentiment data
Invoke-WebRequest -Uri "http://localhost:8000/aggregate" -Method POST
```

**Note**: The system automatically scrapes data every 30 minutes (Reddit) and every hour (news + aggregation).

## Manual Setup (Development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your credentials

# Run database migrations
alembic upgrade head

# Start the backend
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Celery Setup

```bash
# Start Redis
redis-server

# Start Celery worker
celery -A app.celery_app worker --loglevel=info

# Start Celery beat (scheduler)
celery -A app.celery_app beat --loglevel=info
```

## API Endpoints

### Dashboard
- `GET /dashboard` - Get top bullish/bearish stocks
- `GET /stock/{ticker}` - Get detailed stock information
- `GET /sentiment/{ticker}/history` - Get sentiment history
- `GET /mentions/{ticker}` - Get recent mentions

### Data Collection
- `POST /scrape/reddit` - Trigger Reddit scraping
- `POST /scrape/news` - Trigger news scraping
- `POST /aggregate` - Aggregate sentiment data

### Health
- `GET /health` - Health check endpoint

## Data Pipeline

1. **Data Ingestion**
   - Reddit scraper pulls posts/comments from finance subreddits (r/stocks, r/wallstreetbets, r/investing, r/SecurityAnalysis)
   - News API fetches financial headlines and articles
   - Automated scraping every 30 minutes (Reddit) and hourly (news)

2. **Text Processing**
   - Extract stock tickers using regex pattern `$TICKER`
   - Clean text (remove emojis, URLs, extra whitespace)
   - Filter out invalid or non-existent tickers

3. **Sentiment Analysis**
   - Process text through FinBERT model with lazy loading
   - Generate sentiment scores (-1 to 1) and labels (positive/negative/neutral)
   - Handle rate limiting and error recovery

4. **Data Aggregation**
   - Real-time aggregation by ticker
   - Calculate sentiment indices and bullish/bearish scores
   - Generate trending stock rankings with configurable thresholds
   - Store historical data for trend analysis

5. **API & Frontend**
   - RESTful API serves processed data with CORS support
   - React dashboard displays live insights and interactive charts
   - Real-time updates and responsive design

## Configuration

### Reddit API Setup
1. Go to https://www.reddit.com/prefs/apps
2. Create a new application
3. Note the client ID and secret
4. Add to your `.env` file

### News API Setup
1. Sign up at https://newsapi.org/
2. Get your API key
3. Add to your `.env` file

### Database Configuration
The application uses PostgreSQL by default. Update the `DATABASE_URL` in your environment variables if using a different database.

## Deployment

### Production Deployment

1. **Environment Variables**
   ```env
   DATABASE_URL=postgresql://user:password@your-db-host:5432/stock_sentiment
   REDIS_URL=redis://your-redis-host:6379
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   NEWS_API_KEY=your_news_api_key
   ```

2. **Docker Compose Production**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Manual Deployment**
   - Deploy PostgreSQL and Redis
   - Deploy backend with proper environment
   - Deploy frontend with build artifacts
   - Set up reverse proxy (nginx)

## Automated Scheduling

The system includes automated data collection with the following schedule:

- **Reddit Scraping**: Every 30 minutes
- **News Scraping**: Every hour
- **Sentiment Aggregation**: Every hour (15 minutes after news scraping)

### Manual Data Collection

You can manually trigger data collection at any time:

```bash
# Scrape Reddit data
Invoke-WebRequest -Uri "http://localhost:8000/scrape/reddit" -Method POST

# Scrape news data
Invoke-WebRequest -Uri "http://localhost:8000/scrape/news" -Method POST

# Aggregate sentiment data
Invoke-WebRequest -Uri "http://localhost:8000/aggregate" -Method POST

# Full scraping pipeline
Invoke-WebRequest -Uri "http://localhost:8000/scrape/reddit" -Method POST
Invoke-WebRequest -Uri "http://localhost:8000/scrape/news" -Method POST
Invoke-WebRequest -Uri "http://localhost:8000/aggregate" -Method POST
```

## Monitoring

### Health Checks
- Backend: `GET /health`
- Database: Connection status with health checks
- Redis: Ping test with health checks
- Celery: Worker status monitoring

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f celery-worker
docker-compose logs -f celery-beat
```

### Container Status
```bash
# Check container health
docker-compose ps

# View real-time logs
docker-compose logs -f --tail=50
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **Database Tables Missing**
   ```bash
   # Run database migrations
   docker-compose exec backend alembic upgrade head
   ```

2. **Empty Dashboard**
   ```bash
   # Clear sample data and get real data
   docker-compose exec backend python -c "from app.database import SessionLocal; from app.models import *; db = SessionLocal(); db.query(StockMention).delete(); db.query(StockSentiment).delete(); db.query(TrendingStock).delete(); db.commit(); print('Data cleared')"
   
   # Trigger real data collection
   Invoke-WebRequest -Uri "http://localhost:8000/scrape/reddit" -Method POST
   Invoke-WebRequest -Uri "http://localhost:8000/aggregate" -Method POST
   ```

3. **Reddit API Rate Limits**
   - The app respects Reddit's rate limits
   - Consider reducing scraping frequency if needed
   - Check Reddit API credentials in `.env` file

4. **News API Limits**
   - Free tier has 1000 requests/day
   - Monitor usage in News API dashboard
   - Check News API key in `.env` file

5. **Memory Issues**
   - FinBERT model uses lazy loading to reduce memory usage
   - Consider using a GPU for better performance
   - Monitor container memory usage: `docker stats`

6. **Frontend Not Loading Data**
   - Check if backend is healthy: `curl http://localhost:8000/health`
   - Verify API connectivity: `curl http://localhost:8000/dashboard`
   - Check CORS configuration in backend

7. **Celery Tasks Not Running**
   ```bash
   # Check Celery worker status
   docker-compose logs celery-worker
   
   # Restart Celery services
   docker-compose restart celery-worker celery-beat
   ```

### Performance Optimization

1. **Adjust Scraping Frequency**
   - Edit `backend/app/celery_app.py` to change intervals
   - Reduce frequency if hitting API limits

2. **Database Optimization**
   - Add indexes for frequently queried fields
   - Consider data retention policies for old data

3. **Memory Optimization**
   - FinBERT model loads only when needed
   - Consider using smaller models for development

### Support

For issues and questions:
- Check the logs: `docker-compose logs -f`
- Review API documentation: http://localhost:8000/docs
- Test individual components: `docker-compose ps`
- Open an issue on GitHub

## Current Status

✅ **Fully Implemented and Working**
- Real-time Reddit data scraping from 4 finance subreddits
- Live sentiment analysis using FinBERT AI model
- Automated data collection every 30 minutes
- Interactive dashboard with live stock rankings
- Complete Docker containerization with health checks
- Database migrations and proper data persistence
- CORS-enabled API with proper error handling

🎯 **Live Data Sources**
- Reddit: r/stocks, r/wallstreetbets, r/investing, r/SecurityAnalysis
- News API: Financial headlines and articles
- Real-time sentiment scoring and stock rankings

📊 **Dashboard Features**
- Top 5 Bullish stocks with live sentiment scores
- Top 5 Bearish stocks with live sentiment scores
- Real-time mentions count and sentiment indices
- Interactive charts and responsive design
- Automatic data refresh every 30 minutes

🚀 **Ready for Production**
The application is fully functional and ready for deployment with real-time data collection and analysis.
