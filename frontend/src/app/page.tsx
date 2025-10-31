'use client'

import { useEffect, useState } from 'react'
import HeroSection from '@/components/home/HeroSection'
import TrendingSection from '@/components/home/TrendingSection'
import RecommendationsSection from '@/components/home/RecommendationsSection'
import CategoriesSection from '@/components/home/CategoriesSection'
import LocalVendorsSection from '@/components/home/LocalVendorsSection'
import { useUserStore } from '@/store/userStore'

export default function Home() {
  const { user, county } = useUserStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulated loading
    setTimeout(() => setLoading(false), 500)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Banner */}
      <HeroSection />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
        
        {/* Personalized Recommendations */}
        {user && (
          <RecommendationsSection 
            userId={user.id}
            title={`Karibu ${user.name || 'Rafiki'}! Tulikupendekea`}
            titleEn={`Welcome ${user.name || 'Friend'}! Recommended for You`}
          />
        )}

        {/* Trending in Your Area */}
        <TrendingSection 
          county={county || 'Nairobi'}
          title="Trending Karibu Nawe"
          titleEn="Trending Near You"
        />

        {/* Categories */}
        <CategoriesSection />

        {/* Local Vendors */}
        <LocalVendorsSection 
          county={county}
          title="Wafanyabiashara wa Ndani"
          titleEn="Local Kenyan Vendors"
        />

        {/* Smart Picks Based on Time */}
        <RecommendationsSection 
          userId={user?.id}
          contextAware={true}
          title="Chaguo Zako za Sasa"
          titleEn="Smart Picks for You"
        />
      </div>
    </div>
  )
}

