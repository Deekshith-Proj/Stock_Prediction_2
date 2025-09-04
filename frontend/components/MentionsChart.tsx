import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { StockSentiment } from '@/types'

interface MentionsChartProps {
  data: StockSentiment[]
}

export default function MentionsChart({ data }: MentionsChartProps) {
  const chartData = data.map(item => ({
    date: new Date(item.date).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    }),
    positive: item.positive_mentions,
    negative: item.negative_mentions,
    neutral: item.neutral_mentions,
    total: item.mentions_count
  })).reverse() // Show oldest to newest

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            tickLine={{ stroke: '#e5e7eb' }}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            tickLine={{ stroke: '#e5e7eb' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
          />
          <Legend />
          <Bar 
            dataKey="positive" 
            stackId="a" 
            fill="#22c55e" 
            name="Positive"
          />
          <Bar 
            dataKey="negative" 
            stackId="a" 
            fill="#ef4444" 
            name="Negative"
          />
          <Bar 
            dataKey="neutral" 
            stackId="a" 
            fill="#6b7280" 
            name="Neutral"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
