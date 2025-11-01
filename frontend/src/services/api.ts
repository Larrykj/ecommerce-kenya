/**
 * API Service
 * Handles all API requests to the backend
 */
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_V1 = `${API_URL}/api/v1`

const api = axios.create({
  baseURL: API_V1,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (data: any) => api.post('/auth/register', data),
  login: (data: any) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me')
}

export const productsAPI = {
  list: (params: any) => api.get('/products', { params }),
  get: (id: string) => api.get(`/products/${id}`),
  getCategories: () => api.get('/products/categories/list'),
  getLocalVendors: (county?: string) => api.get('/products/vendors/local', { 
    params: { county } 
  })
}

export const recommendationsAPI = {
  getPersonalized: (userId: string, params: any) => 
    api.post('/recommendations/personalized', null, { params: { user_id: userId, ...params } }),
  getSimilar: (productId: string, params: any) =>
    api.get(`/recommendations/similar/${productId}`, { params }),
  getTrending: (params: any) =>
    api.get('/recommendations/trending', { params }),
  getBundle: (productIds: string[]) =>
    api.get('/recommendations/bundle', { params: { product_ids: productIds } }),
  getContextAware: (userId: string, context: any) =>
    api.post('/recommendations/context-aware', null, { 
      params: { user_id: userId, ...context } 
    }),
  getSearchSuggestions: (query: string, language: string = 'en') =>
    api.get('/recommendations/search/suggestions', { params: { query, language } }),
  getHomepage: (userId: string, county?: string) =>
    api.get(`/recommendations/homepage/${userId}`, { params: { county } })
}

export const ordersAPI = {
  create: (data: any) => api.post('/orders', data),
  get: (orderId: string) => api.get(`/orders/${orderId}`),
  list: (userId: string) => api.get(`/orders/user/${userId}`),
  cancel: (orderId: string) => api.put(`/orders/${orderId}/cancel`)
}

export const mpesaAPI = {
  initiateSTKPush: (data: any) => api.post('/mpesa/stk-push', data),
  queryStatus: (checkoutRequestId: string) => 
    api.get(`/mpesa/query/${checkoutRequestId}`)
}

export const analyticsAPI = {
  trackEvent: (data: any) => api.post('/analytics/track', data),
  getDashboard: (params: any) => api.get('/analytics/dashboard', { params }),
  getCountyInsights: (county: string) => 
    api.get('/analytics/county-insights', { params: { county } })
}

export default api

