'use client'

import { useEffect, useState } from 'react'
import { useLanguageStore } from '@/store/languageStore'
import ProductCard from '@/components/products/ProductCard'
import axios from 'axios'

interface Product {
  id: string
  name: string
  name_sw?: string
  price: number
  image?: string
  images?: string[]
  average_rating?: number
  is_local_vendor?: boolean
}

export default function TrendingPage() {
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTrendingProducts = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${API_URL}/api/v1/products`)
        const productsData = response.data.products.map((p: any) => ({
          ...p,
          image: p.images?.[0] || p.thumbnail
        }))
        setProducts(productsData)
      } catch (error) {
        console.error('Failed to fetch trending products:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTrendingProducts()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center mb-8">
          <span className="text-4xl mr-3">🔥</span>
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
              {isSwahili ? 'Vinavyopendwa Sana' : 'Trending Now'}
            </h1>
            <p className="text-gray-600 mt-1">
              {isSwahili 
                ? 'Bidhaa zinazopendwa zaidi katika Kenya sasa hivi'
                : 'Most popular products in Kenya right now'}
            </p>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          </div>
        ) : products.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">🔥</div>
            <p className="text-gray-600">
              {isSwahili 
                ? 'Hakuna bidhaa zinazopatikana kwa sasa'
                : 'No trending products available'}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

