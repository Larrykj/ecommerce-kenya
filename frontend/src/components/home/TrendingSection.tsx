'use client'

import { useEffect, useState } from 'react'
import ProductCard from '../products/ProductCard'
import { useLanguageStore } from '@/store/languageStore'

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
    // Fetch trending products from API
    // For now, mock data
    setTimeout(() => {
      setProducts([])
      setLoading(false)
    }, 1000)
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

