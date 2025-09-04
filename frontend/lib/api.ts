import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const apiClient = {
  // Dashboard
  getDashboard: () => api.get('/dashboard'),
  
  // Stock details
  getStockDetail: (ticker: string) => api.get(`/stock/${ticker}`),
  getSentimentHistory: (ticker: string, days: number = 7) => 
    api.get(`/sentiment/${ticker}/history?days=${days}`),
  getStockMentions: (ticker: string, limit: number = 50) => 
    api.get(`/mentions/${ticker}?limit=${limit}`),
  
  // Scraping endpoints
  scrapeReddit: () => api.post('/scrape/reddit'),
  scrapeNews: () => api.post('/scrape/news'),
  aggregateSentiment: () => api.post('/aggregate'),
  
  // Health check
  healthCheck: () => api.get('/health'),
}

export { api }
