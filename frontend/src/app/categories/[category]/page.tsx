'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
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
  category: string
}

const categoryData = {
  electronics: { nameEn: 'Electronics', nameSw: 'Elektroniki', icon: '📱' },
  fashion: { nameEn: 'Fashion', nameSw: 'Mitindo', icon: '👗' },
  home: { nameEn: 'Home & Living', nameSw: 'Nyumbani', icon: '🏠' },
  beauty: { nameEn: 'Beauty & Health', nameSw: 'Urembo na Afya', icon: '💄' },
  food: { nameEn: 'Food & Groceries', nameSw: 'Chakula', icon: '🍎' },
  sports: { nameEn: 'Sports', nameSw: 'Michezo', icon: '⚽' },
  books: { nameEn: 'Books & Media', nameSw: 'Vitabu', icon: '📚' },
  toys: { nameEn: 'Toys & Kids', nameSw: 'Watoto', icon: '🧸' },
}

export default function CategoryPage() {
  const params = useParams()
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'
  
  const category = params.category as string
  const categoryInfo = categoryData[category as keyof typeof categoryData]
  
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchCategoryProducts = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${API_URL}/api/v1/products`, {
          params: { category: category }
        })
        const productsData = response.data.products.map((p: any) => ({
          ...p,
          image: p.images?.[0] || p.thumbnail
        }))
        setProducts(productsData)
      } catch (error) {
        console.error('Failed to fetch category products:', error)
      } finally {
        setLoading(false)
      }
    }

    if (categoryInfo) {
      fetchCategoryProducts()
    }
  }, [category, categoryInfo])

  if (!categoryInfo) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {isSwahili ? 'Kategoria haijapatikana' : 'Category not found'}
          </h1>
          <a href="/categories" className="btn-primary">
            {isSwahili ? 'Rudi kwenye Kategoria' : 'Back to Categories'}
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Category Header */}
        <div className="flex items-center mb-8">
          <div className="text-4xl mr-4">{categoryInfo.icon}</div>
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
              {isSwahili ? categoryInfo.nameSw : categoryInfo.nameEn}
            </h1>
            <p className="text-gray-600 mt-2">
              {isSwahili 
                ? 'Bidhaa bora katika kategoria hii'
                : 'Best products in this category'}
            </p>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isSwahili ? 'Bei' : 'Price'}
              </label>
              <select className="input-field">
                <option>{isSwahili ? 'Zote' : 'All'}</option>
                <option>KES 0 - 1,000</option>
                <option>KES 1,000 - 5,000</option>
                <option>KES 5,000 - 20,000</option>
                <option>KES 20,000+</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isSwahili ? 'Chapa' : 'Brand'}
              </label>
              <select className="input-field">
                <option>{isSwahili ? 'Zote' : 'All'}</option>
                <option>Samsung</option>
                <option>Apple</option>
                <option>Huawei</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isSwahili ? 'Ukadiriaji' : 'Rating'}
              </label>
              <select className="input-field">
                <option>{isSwahili ? 'Zote' : 'All'}</option>
                <option>4+ ★</option>
                <option>3+ ★</option>
                <option>2+ ★</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isSwahili ? 'Panga kwa' : 'Sort by'}
              </label>
              <select className="input-field">
                <option>{isSwahili ? 'Maarufu' : 'Popular'}</option>
                <option>{isSwahili ? 'Bei ya chini' : 'Price: Low to High'}</option>
                <option>{isSwahili ? 'Bei ya juu' : 'Price: High to Low'}</option>
                <option>{isSwahili ? 'Ukadiriaji' : 'Rating'}</option>
              </select>
            </div>
          </div>
        </div>

        {/* Products Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          </div>
        ) : products.length > 0 ? (
          <div>
            <p className="text-gray-600 mb-6">
              {products.length} {isSwahili ? 'bidhaa zimepatikana' : 'products found'}
            </p>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">{categoryInfo.icon}</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              {isSwahili ? 'Hakuna bidhaa katika kategoria hii' : 'No products in this category'}
            </h2>
            <p className="text-gray-600 mb-6">
              {isSwahili 
                ? `Tunaongeza bidhaa za ${categoryInfo.nameSw} kila siku.`
                : `We're adding new ${categoryInfo.nameEn.toLowerCase()} products daily.`}
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
