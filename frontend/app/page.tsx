'use client'

import { useState, useEffect } from 'react'
import { TrendingUp, TrendingDown, RefreshCw, BarChart3 } from 'lucide-react'
import { DashboardData, TrendingStock } from '@/types'
import { apiClient } from '@/lib/api'
import StockCard from '@/components/StockCard'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = async () => {
    try {
      setError(null)
      const response = await apiClient.getDashboard()
      setData(response.data)
    } catch (err) {
      setError('Failed to fetch dashboard data')
      console.error('Error fetching dashboard data:', err)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  const handleRefresh = async () => {
    setRefreshing(true)
    await fetchData()
  }

  useEffect(() => {
    fetchData()
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Stock Sentiment Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Real-time sentiment analysis from Reddit and news sources
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="btn btn-primary flex items-center space-x-2"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-bullish-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-bullish-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Bullish Stocks</p>
              <p className="text-2xl font-bold text-gray-900">
                {data?.bullish_stocks.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-bearish-100 rounded-lg">
              <TrendingDown className="w-6 h-6 text-bearish-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Bearish Stocks</p>
              <p className="text-2xl font-bold text-gray-900">
                {data?.bearish_stocks.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Last Updated</p>
              <p className="text-sm font-bold text-gray-900">
                {data?.last_updated 
                  ? new Date(data.last_updated).toLocaleTimeString()
                  : 'Never'
                }
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stock Lists */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bullish Stocks */}
        <div className="card">
          <div className="card-header flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-bullish-600" />
            <span>Top Bullish Stocks</span>
          </div>
          <div className="space-y-3">
            {data?.bullish_stocks.length ? (
              data.bullish_stocks.map((stock, index) => (
                <StockCard
                  key={`bullish-${stock.ticker}`}
                  stock={stock}
                  rank={index + 1}
                  type="bullish"
                />
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">
                No bullish stocks data available
              </p>
            )}
          </div>
        </div>

        {/* Bearish Stocks */}
        <div className="card">
          <div className="card-header flex items-center space-x-2">
            <TrendingDown className="w-5 h-5 text-bearish-600" />
            <span>Top Bearish Stocks</span>
          </div>
          <div className="space-y-3">
            {data?.bearish_stocks.length ? (
              data.bearish_stocks.map((stock, index) => (
                <StockCard
                  key={`bearish-${stock.ticker}`}
                  stock={stock}
                  rank={index + 1}
                  type="bearish"
                />
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">
                No bearish stocks data available
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
