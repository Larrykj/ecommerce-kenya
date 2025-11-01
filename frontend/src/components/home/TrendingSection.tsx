'use client'

import { useEffect, useState } from 'react'
import ProductCard from '../products/ProductCard'
import { useLanguageStore } from '@/store/languageStore'
import { recommendationsAPI } from '@/services/api'

interface TrendingSectionProps {
  county: string
  title: string
  titleEn: string
}

export default function TrendingSection({ county, title, titleEn }: TrendingSectionProps) {
  const { language } = useLanguageStore()
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTrending = async () => {
      try {
        setLoading(true)
        const response = await recommendationsAPI.getTrending({ 
          county: county || undefined, 
          limit: 10 
        })
        if (response.data?.products) {
          setProducts(response.data.products)
        }
      } catch (error) {
        console.error('Failed to fetch trending products:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTrending()
  }, [county])

  return (
    <section>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900">
            {language === 'sw' ? title : titleEn}
          </h2>
          <p className="text-gray-600 mt-1">
            {language === 'sw' 
              ? `Vitu vinavyoongoza ${county}` 
              : `What's hot in ${county}`}
          </p>
        </div>
        <button className="text-primary-600 font-semibold hover:text-primary-700">
          {language === 'sw' ? 'Tazama Zaidi →' : 'View All →'}
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="spinner"></div>
        </div>
      ) : products.length === 0 ? (
        <div className="bg-gray-100 rounded-lg p-12 text-center">
          <p className="text-gray-600">
            {language === 'sw' 
              ? 'Hakuna bidhaa za kawaida kwa sasa' 
              : 'No trending products at the moment'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {products.map((product: any) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </section>
  )
}

