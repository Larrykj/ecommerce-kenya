'use client'

import { useEffect, useState } from 'react'
import { useLanguageStore } from '@/store/languageStore'
import { useUserStore } from '@/store/userStore'

export default function LocalVendorsPage() {
  const { language } = useLanguageStore()
  const { county } = useUserStore()
  const isSwahili = language === 'sw'
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate loading vendors
    setTimeout(() => setLoading(false), 1000)
  }, [])

  const vendors = [
    {
      id: 1,
      name: 'Nairobi Electronics Hub',
      name_sw: 'Kituo cha Elektroniki Nairobi',
      county: 'Nairobi',
      category: 'Electronics',
      rating: 4.8,
      products: 250,
      verified: true
    },
    {
      id: 2,
      name: 'Mombasa Fashion House',
      name_sw: 'Nyumba ya Mitindo Mombasa',
      county: 'Mombasa',
      category: 'Fashion',
      rating: 4.6,
      products: 180,
      verified: true
    },
    {
      id: 3,
      name: 'Kisumu Fresh Foods',
      name_sw: 'Chakula Safi Kisumu',
      county: 'Kisumu',
      category: 'Food & Groceries',
      rating: 4.9,
      products: 120,
      verified: true
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-kenyan-green to-green-700 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            🇰🇪 {isSwahili ? 'Wafanyabiashara wa Ndani' : 'Local Kenyan Vendors'}
          </h1>
          <p className="text-xl text-green-100">
            {isSwahili 
              ? 'Unga mkono biashara za Wakenya. Nunua kutoka kwa wazalishaji na wauzaji wa ndani.'
              : 'Support Kenyan businesses. Buy directly from local producers and sellers.'}
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        {/* Filter Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isSwahili ? 'Kaunti' : 'County'}
              </label>
              <select className="input-field">
                <option>{isSwahili ? 'Zote' : 'All'}</option>
                <option>Nairobi</option>
                <option>Mombasa</option>
                <option>Kisumu</option>
                <option>Nakuru</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isSwahili ? 'Kategoria' : 'Category'}
              </label>
              <select className="input-field">
                <option>{isSwahili ? 'Zote' : 'All'}</option>
                <option>Electronics</option>
                <option>Fashion</option>
                <option>Food & Groceries</option>
                <option>Home & Living</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isSwahili ? 'Panga kwa' : 'Sort by'}
              </label>
              <select className="input-field">
                <option>{isSwahili ? 'Ukadiriaji' : 'Rating'}</option>
                <option>{isSwahili ? 'Bidhaa Nyingi' : 'Most Products'}</option>
                <option>{isSwahili ? 'Jina' : 'Name'}</option>
              </select>
            </div>
          </div>
        </div>

        {/* Vendors Grid */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="spinner"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {vendors.map((vendor) => (
              <div key={vendor.id} className="card overflow-hidden">
                {/* Vendor Header */}
                <div className="bg-gradient-to-r from-green-50 to-green-100 p-6">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-xl font-bold text-gray-900">
                      {isSwahili && vendor.name_sw ? vendor.name_sw : vendor.name}
                    </h3>
                    {vendor.verified && (
                      <span className="bg-green-600 text-white text-xs px-2 py-1 rounded-full">
                        ✓ {isSwahili ? 'Imethhibitishwa' : 'Verified'}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600">
                    📍 {vendor.county}
                  </p>
                </div>

                {/* Vendor Info */}
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className="flex items-center text-yellow-400 mb-1">
                        <span className="text-lg">★</span>
                        <span className="text-gray-900 ml-1 font-semibold">{vendor.rating}</span>
                      </div>
                      <p className="text-xs text-gray-500">
                        {vendor.products} {isSwahili ? 'bidhaa' : 'products'}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-700">{vendor.category}</p>
                    </div>
                  </div>

                  <a href={`/vendors/${vendor.id}`} className="block w-full">
                    <button className="w-full btn-primary">
                      {isSwahili ? 'Tazama Duka' : 'View Store'}
                    </button>
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-kenyan-red/10 to-kenyan-green/10 rounded-2xl p-8 mt-12 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            {isSwahili ? 'Je, una biashara?' : 'Are you a business owner?'}
          </h2>
          <p className="text-gray-700 mb-6">
            {isSwahili
              ? 'Jiunge na mfumo wetu na uanzie kuuza bidhaa zako kwa wateja zaidi.'
              : 'Join our platform and start selling your products to more customers.'}
          </p>
          <button className="btn-primary text-lg px-8 py-3">
            {isSwahili ? 'Jiunge kama Muuzaji' : 'Become a Vendor'}
          </button>
        </div>
      </div>
    </div>
  )
}

