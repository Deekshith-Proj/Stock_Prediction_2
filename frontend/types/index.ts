export interface StockMention {
  id: number
  ticker: string
  text: string
  sentiment: 'positive' | 'negative' | 'neutral'
  sentiment_score: number
  source: 'reddit' | 'news'
  source_id?: string
  created_at: string
  processed_at: string
}

export interface StockSentiment {
  id: number
  ticker: string
  date: string
  mentions_count: number
  positive_mentions: number
  negative_mentions: number
  neutral_mentions: number
  sentiment_index: number
  bullish_score: number
  bearish_score: number
  created_at: string
}

export interface TrendingStock {
  id: number
  ticker: string
  rank: number
  category: 'bullish' | 'bearish'
  score: number
  mentions_count: number
  sentiment_index: number
  date: string
  created_at: string
}

export interface DashboardData {
  bullish_stocks: TrendingStock[]
  bearish_stocks: TrendingStock[]
  last_updated: string
}

export interface StockDetailData {
  ticker: string
  current_sentiment: StockSentiment
  historical_sentiment: StockSentiment[]
  recent_mentions: StockMention[]
}

export interface SentimentHistoryData {
  ticker: string
  history: StockSentiment[]
  days: number
}

export interface StockMentionsData {
  ticker: string
  mentions: StockMention[]
  count: number
}
