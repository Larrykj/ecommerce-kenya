'use client'

import Link from 'next/link'
import { useLanguageStore } from '@/store/languageStore'

export default function HeroSection() {
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'

  return (
    <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <div className="grid md:grid-cols-2 gap-8 items-center">
          
          {/* Text Content */}
          <div className="space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold leading-tight">
              {isSwahili 
                ? 'Nunua Bidhaa Bora, Tulizopendekezwa Kwako'
                : 'Discover Products Tailored Just for You'}
            </h1>
            <p className="text-lg md:text-xl text-primary-100">
              {isSwahili
                ? 'Teknolojia ya AI inayokupa mapendekezo maalum kulingana na mahitaji yako. Ununue haraka, ununue salama, kutoka popote Kenya.'
                : 'AI-powered recommendations that understand your needs. Shop fast, shop safe, anywhere in Kenya.'}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <Link 
                href="/categories" 
                className="bg-white text-primary-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition text-center"
              >
                {isSwahili ? 'Tazama Kategoria' : 'Browse Categories'}
              </Link>
              <Link 
                href="/trending" 
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-700 transition text-center"
              >
                {isSwahili ? 'Vya Kuvutia Sasa' : 'Trending Now'}
              </Link>
            </div>

            {/* Features */}
            <div className="grid grid-cols-3 gap-4 pt-8 border-t border-primary-500">
              <div className="text-center">
                <div className="text-2xl font-bold">🚚</div>
                <p className="text-sm mt-2">{isSwahili ? 'Usafirishaji Kila Mahali' : 'Countrywide Delivery'}</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">💳</div>
                <p className="text-sm mt-2">{isSwahili ? 'Lipa na M-Pesa' : 'M-Pesa Payments'}</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">🏪</div>
                <p className="text-sm mt-2">{isSwahili ? 'Wafanyabiashara wa Ndani' : 'Local Vendors'}</p>
              </div>
            </div>
          </div>

          {/* Image/Illustration */}
          <div className="hidden md:block">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 shadow-2xl">
              <div className="aspect-square bg-gradient-to-br from-white/20 to-white/5 rounded-xl flex items-center justify-center">
                <div className="text-center">
                  <div className="text-6xl mb-4">🛍️</div>
                  <p className="text-white/80 text-lg">
                    {isSwahili ? 'Milioni ya bidhaa' : 'Millions of products'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

