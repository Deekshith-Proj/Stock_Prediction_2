'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { ArrowLeft, TrendingUp, TrendingDown, MessageSquare, Calendar, ExternalLink } from 'lucide-react'
import Link from 'next/link'
import { StockDetailData, SentimentHistoryData, StockMentionsData } from '@/types'
import { apiClient } from '@/lib/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import SentimentChart from '@/components/SentimentChart'
import MentionsChart from '@/components/MentionsChart'
import MentionCard from '@/components/MentionCard'

export default function StockDetailPage() {
  const params = useParams()
  const ticker = params.ticker as string
  
  const [stockData, setStockData] = useState<StockDetailData | null>(null)
  const [sentimentHistory, setSentimentHistory] = useState<SentimentHistoryData | null>(null)
  const [mentions, setMentions] = useState<StockMentionsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchStockData = async () => {
    try {
      setError(null)
      const [detailResponse, historyResponse, mentionsResponse] = await Promise.all([
        apiClient.getStockDetail(ticker),
        apiClient.getSentimentHistory(ticker, 7),
        apiClient.getStockMentions(ticker, 20)
      ])
      
      setStockData(detailResponse.data)
      setSentimentHistory(historyResponse.data)
      setMentions(mentionsResponse.data)
    } catch (err) {
      setError('Failed to fetch stock data')
      console.error('Error fetching stock data:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (ticker) {
      fetchStockData()
    }
  }, [ticker])

  if (loading) {
    return <LoadingSpinner text={`Loading ${ticker} data...`} />
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchStockData} />
  }

  if (!stockData) {
    return <ErrorMessage message="Stock not found" />
  }

  const { current_sentiment, historical_sentiment } = stockData
  const isBullish = current_sentiment.sentiment_index > 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Link 
          href="/"
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-5 h-5 text-gray-600" />
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">${ticker}</h1>
          <div className="flex items-center space-x-2 mt-1">
            {isBullish ? (
              <TrendingUp className="w-5 h-5 text-bullish-600" />
            ) : (
              <TrendingDown className="w-5 h-5 text-bearish-600" />
            )}
            <span className={`font-medium ${
              isBullish ? 'text-bullish-600' : 'text-bearish-600'
            }`}>
              {isBullish ? 'Bullish' : 'Bearish'} Sentiment
            </span>
          </div>
        </div>
      </div>

      {/* Current Sentiment Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">
              {current_sentiment.mentions_count}
            </div>
            <div className="text-sm text-gray-600">Total Mentions</div>
          </div>
        </div>
        
        <div className="card">
          <div className="text-center">
            <div className="text-2xl font-bold text-bullish-600">
              {current_sentiment.positive_mentions}
            </div>
            <div className="text-sm text-gray-600">Positive</div>
          </div>
        </div>
        
        <div className="card">
          <div className="text-center">
            <div className="text-2xl font-bold text-bearish-600">
              {current_sentiment.negative_mentions}
            </div>
            <div className="text-sm text-gray-600">Negative</div>
          </div>
        </div>
        
        <div className="card">
          <div className="text-center">
            <div className={`text-2xl font-bold ${
              current_sentiment.sentiment_index > 0 ? 'text-bullish-600' : 'text-bearish-600'
            }`}>
              {current_sentiment.sentiment_index > 0 ? '+' : ''}{current_sentiment.sentiment_index.toFixed(2)}
            </div>
            <div className="text-sm text-gray-600">Sentiment Index</div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">Sentiment Trend (7 Days)</div>
          <SentimentChart data={historical_sentiment} />
        </div>
        
        <div className="card">
          <div className="card-header">Mentions Volume (7 Days)</div>
          <MentionsChart data={historical_sentiment} />
        </div>
      </div>

      {/* Recent Mentions */}
      <div className="card">
        <div className="card-header flex items-center space-x-2">
          <MessageSquare className="w-5 h-5 text-gray-600" />
          <span>Recent Mentions</span>
        </div>
        <div className="space-y-3">
          {mentions?.mentions.length ? (
            mentions.mentions.map((mention) => (
              <MentionCard key={mention.id} mention={mention} />
            ))
          ) : (
            <p className="text-gray-500 text-center py-4">
              No recent mentions found
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
