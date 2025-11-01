'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
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
  vendor_name?: string
}

const vendorData: Record<string, any> = {
  '1': {
    name: 'Nairobi Electronics Hub',
    name_sw: 'Kituo cha Elektroniki Nairobi',
    county: 'Nairobi',
    category: 'Electronics',
    rating: 4.8,
    verified: true,
    description: 'Leading electronics supplier in Nairobi offering the latest smartphones, laptops, and accessories.',
    description_sw: 'Muuzaji mkuu wa elektroniki huko Nairobi anayetoa simu za mkononi za kisasa, kompyuta za kubebea, na vifaa.'
  },
  '2': {
    name: 'Mombasa Fashion House',
    name_sw: 'Nyumba ya Mitindo Mombasa',
    county: 'Mombasa',
    category: 'Fashion',
    rating: 4.6,
    verified: true,
    description: 'Premium fashion boutique specializing in traditional and modern African wear.',
    description_sw: 'Duka la mitindo la hali ya juu linalojihusisha na mavazi ya Kiafrika ya jadi na ya kisasa.'
  },
  '3': {
    name: 'Kisumu Fresh Foods',
    name_sw: 'Chakula Safi Kisumu',
    county: 'Kisumu',
    category: 'Food & Groceries',
    rating: 4.9,
    verified: true,
    description: 'Fresh organic produce and local food products from Lake Victoria region.',
    description_sw: 'Mazao safi ya kikaboni na bidhaa za chakula za ndani kutoka kanda ya Ziwa Victoria.'
  }
}

export default function VendorStorePage() {
  const params = useParams()
  const router = useRouter()
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'
  const vendorId = params.vendorId as string

  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  const vendor = vendorData[vendorId]

  useEffect(() => {
    const fetchVendorProducts = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${API_URL}/api/v1/products`)
        // Filter by vendor or show all products
        const productsData = response.data.products.map((p: any) => ({
          ...p,
          image: p.images?.[0] || p.thumbnail
        }))
        setProducts(productsData)
      } catch (error) {
        console.error('Failed to fetch vendor products:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchVendorProducts()
  }, [])

  if (!vendor) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {isSwahili ? 'Muuzaji hajapatikana' : 'Vendor not found'}
          </h1>
          <button onClick={() => router.push('/local-vendors')} className="btn-primary">
            {isSwahili ? 'Rudi kwa Wafanyabiashara' : 'Back to Vendors'}
          </button>
        </div>
      </div>
    )
  }

  const displayName = isSwahili && vendor.name_sw ? vendor.name_sw : vendor.name
  const displayDescription = isSwahili && vendor.description_sw ? vendor.description_sw : vendor.description

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Vendor Header */}
      <div className="bg-gradient-to-r from-green-600 to-green-700 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                <h1 className="text-4xl font-bold">{displayName}</h1>
                {vendor.verified && (
                  <span className="bg-white text-green-600 text-sm px-3 py-1 rounded-full font-semibold">
                    ✓ {isSwahili ? 'Imethhibitishwa' : 'Verified'}
                  </span>
                )}
              </div>
              <p className="text-green-100 text-lg mb-4">{displayDescription}</p>
              <div className="flex items-center gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <span>📍</span>
                  <span>{vendor.county}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span>★</span>
                  <span>{vendor.rating} {isSwahili ? 'Ukadiriaji' : 'Rating'}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span>🏷️</span>
                  <span>{vendor.category}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Products Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {isSwahili ? 'Bidhaa' : 'Products'}
            </h2>
            {products.length > 0 && (
              <p className="text-gray-600 mt-1">
                {products.length} {isSwahili ? 'bidhaa zinapatikana' : 'products available'}
              </p>
            )}
          </div>
          <button
            onClick={() => router.push('/local-vendors')}
            className="text-gray-600 hover:text-gray-900"
          >
            ← {isSwahili ? 'Rudi' : 'Back'}
          </button>
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
            <div className="text-6xl mb-4">📦</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              {isSwahili ? 'Hakuna bidhaa bado' : 'No products yet'}
            </h3>
            <p className="text-gray-600 mb-6">
              {isSwahili 
                ? 'Muuzaji huyu ataongeza bidhaa hivi karibuni.'
                : 'This vendor will be adding products soon.'}
            </p>
          </div>
        )}

        {/* Contact Section */}
        <div className="bg-white rounded-lg shadow-md p-8 mt-12">
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            {isSwahili ? 'Wasiliana na Muuzaji' : 'Contact Vendor'}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <button className="flex items-center justify-center gap-2 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700">
              📞 {isSwahili ? 'Piga Simu' : 'Call'}
            </button>
            <button className="flex items-center justify-center gap-2 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700">
              💬 {isSwahili ? 'Tuma Ujumbe' : 'Message'}
            </button>
            <button className="flex items-center justify-center gap-2 border-2 border-gray-300 py-3 rounded-lg hover:bg-gray-50">
              📧 {isSwahili ? 'Barua Pepe' : 'Email'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
