import { RefreshCw } from 'lucide-react'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  text?: string
}

export default function LoadingSpinner({ size = 'md', text = 'Loading...' }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  }

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <RefreshCw className={`${sizeClasses[size]} text-blue-600 animate-spin mb-4`} />
      <p className="text-gray-600">{text}</p>
    </div>
  )
}
