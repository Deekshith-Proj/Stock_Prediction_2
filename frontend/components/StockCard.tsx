import { TrendingUp, TrendingDown, MessageSquare, BarChart3 } from 'lucide-react'
import { TrendingStock } from '@/types'
import { clsx } from 'clsx'

interface StockCardProps {
  stock: TrendingStock
  rank: number
  type: 'bullish' | 'bearish'
  onClick?: () => void
}

export default function StockCard({ stock, rank, type, onClick }: StockCardProps) {
  const isBullish = type === 'bullish'
  
  return (
    <div 
      className={clsx(
        'p-4 rounded-lg border-2 transition-all duration-200 hover:shadow-md cursor-pointer',
        isBullish 
          ? 'border-bullish-200 bg-bullish-50 hover:border-bullish-300' 
          : 'border-bearish-200 bg-bearish-50 hover:border-bearish-300'
      )}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={clsx(
            'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white',
            isBullish ? 'bg-bullish-600' : 'bg-bearish-600'
          )}>
            {rank}
          </div>
          <div>
            <h3 className="font-bold text-lg text-gray-900">${stock.ticker}</h3>
            <div className="flex items-center space-x-1">
              {isBullish ? (
                <TrendingUp className="w-4 h-4 text-bullish-600" />
              ) : (
                <TrendingDown className="w-4 h-4 text-bearish-600" />
              )}
              <span className={clsx(
                'text-sm font-medium',
                isBullish ? 'text-bullish-600' : 'text-bearish-600'
              )}>
                {isBullish ? 'Bullish' : 'Bearish'}
              </span>
            </div>
          </div>
        </div>
        
        <div className="text-right">
          <div className="text-lg font-bold text-gray-900">
            {stock.score.toFixed(2)}
          </div>
          <div className="text-sm text-gray-600">Score</div>
        </div>
      </div>
      
      <div className="mt-3 grid grid-cols-2 gap-4">
        <div className="flex items-center space-x-2">
          <MessageSquare className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">
            {stock.mentions_count} mentions
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">
            {stock.sentiment_index > 0 ? '+' : ''}{stock.sentiment_index.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  )
}
