import { MessageSquare, Calendar, ExternalLink } from 'lucide-react'
import { StockMention } from '@/types'
import { clsx } from 'clsx'

interface MentionCardProps {
  mention: StockMention
}

export default function MentionCard({ mention }: MentionCardProps) {
  const isPositive = mention.sentiment === 'positive'
  const isNegative = mention.sentiment === 'negative'
  const isNeutral = mention.sentiment === 'neutral'

  const getSentimentColor = () => {
    if (isPositive) return 'text-bullish-600 bg-bullish-50 border-bullish-200'
    if (isNegative) return 'text-bearish-600 bg-bearish-50 border-bearish-200'
    return 'text-gray-600 bg-gray-50 border-gray-200'
  }

  const getSourceIcon = () => {
    if (mention.source === 'reddit') {
      return '🔴'
    }
    return '📰'
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const truncateText = (text: string, maxLength: number = 200) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center space-x-2">
          <span className="text-lg">{getSourceIcon()}</span>
          <span className="text-sm font-medium text-gray-600 capitalize">
            {mention.source}
          </span>
          <span className="text-xs text-gray-500">
            {formatDate(mention.created_at)}
          </span>
        </div>
        
        <div className={clsx(
          'px-2 py-1 rounded-full text-xs font-medium border',
          getSentimentColor()
        )}>
          {mention.sentiment}
        </div>
      </div>
      
      <p className="text-gray-800 text-sm leading-relaxed mb-3">
        {truncateText(mention.text)}
      </p>
      
      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center space-x-4">
          <span>Score: {mention.sentiment_score.toFixed(2)}</span>
          <span>ID: {mention.source_id}</span>
        </div>
        
        {mention.source === 'reddit' && mention.source_id && (
          <a
            href={`https://reddit.com/comments/${mention.source_id}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 text-blue-600 hover:text-blue-800"
          >
            <ExternalLink className="w-3 h-3" />
            <span>View on Reddit</span>
          </a>
        )}
      </div>
    </div>
  )
}
