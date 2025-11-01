'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
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

export default function SearchPage() {
  const searchParams = useSearchParams()
  const query = searchParams.get('q') || ''
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSearchResults = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${API_URL}/api/v1/products`, {
          params: { search: query }
        })
        const productsData = response.data.products.map((p: any) => ({
          ...p,
          image: p.images?.[0] || p.thumbnail
        }))
        setProducts(productsData)
      } catch (error) {
        console.error('Failed to fetch search results:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSearchResults()
  }, [query])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          {isSwahili ? 'Matokeo ya Utafutaji' : 'Search Results'}
        </h1>
        
        {query && (
          <p className="text-gray-600 mb-8">
            {isSwahili ? 'Ulitafuta:' : 'You searched for:'} <span className="font-semibold">"{query}"</span>
            {products.length > 0 && ` - ${products.length} ${isSwahili ? 'bidhaa' : 'products'} ${isSwahili ? 'zimepatikana' : 'found'}`}
          </p>
        )}

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
            <div className="text-6xl mb-4">🔍</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              {isSwahili ? 'Hakuna matokeo yalipatikana' : 'No results found'}
            </h2>
            <p className="text-gray-600 mb-6">
              {isSwahili 
                ? `Hakukuwa na bidhaa zinazolingana na "${query}"`
                : `No products match your search for "${query}"`}
            </p>
            <a href="/" className="btn-primary inline-block">
              {isSwahili ? 'Rudi Nyumbani' : 'Back to Home'}
            </a>
          </div>
        )}
      </div>
    </div>
  )
}
