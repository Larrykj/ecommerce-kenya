'use client'

import { useEffect, useState } from 'react'
import ProductCard from '../products/ProductCard'
import { useLanguageStore } from '@/store/languageStore'
import { recommendationsAPI } from '@/services/api'

interface RecommendationsSectionProps {
  userId?: string
  contextAware?: boolean
  title: string
  titleEn: string
}

export default function RecommendationsSection({ 
  userId, 
  contextAware = false,
  title, 
  titleEn 
}: RecommendationsSectionProps) {
  const { language } = useLanguageStore()
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) {
      setLoading(false)
      return
    }

    const fetchRecommendations = async () => {
      try {
        setLoading(true)
        let response
        
        if (contextAware) {
          // Use context-aware recommendations
          const timeOfDay = new Date().getHours() < 12 ? 'morning' : 
                           new Date().getHours() < 18 ? 'afternoon' : 'evening'
          response = await recommendationsAPI.getContextAware(userId, {
            time_of_day: timeOfDay,
            limit: 10
          })
        } else {
          // Use personalized recommendations
          response = await recommendationsAPI.getPersonalized(userId, {
            limit: 10,
            algorithm: 'hybrid'
          })
        }
        
        if (response.data?.products) {
          setRecommendations(response.data.products)
        }
      } catch (error) {
        console.error('Failed to fetch recommendations:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchRecommendations()
  }, [userId, contextAware])

  if (!userId) {
    return null
  }

  return (
    <section>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900">
            {language === 'sw' ? title : titleEn}
          </h2>
          <p className="text-gray-600 mt-1">
            {language === 'sw' 
              ? 'Kulingana na historia yako ya ununuzi' 
              : 'Based on your browsing and purchase history'}
          </p>
        </div>
        <button className="text-primary-600 font-semibold hover:text-primary-700">
          {language === 'sw' ? 'Onyesha Zaidi →' : 'Show More →'}
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="spinner"></div>
        </div>
      ) : recommendations.length === 0 ? (
        <div className="bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg p-12 text-center">
          <div className="text-4xl mb-4">🎯</div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {language === 'sw' 
              ? 'Mapendekezo yako yanakuja!' 
              : 'Your recommendations are on the way!'}
          </h3>
          <p className="text-gray-600">
            {language === 'sw'
              ? 'Tazama bidhaa zaidi ili tupate kujua unachopenda'
              : 'Browse more products to help us understand your preferences'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {recommendations.map((product: any) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </section>
  )
}

