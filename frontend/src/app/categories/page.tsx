'use client'

import Link from 'next/link'
import { useLanguageStore } from '@/store/languageStore'

const categories = [
  { id: 'electronics', nameEn: 'Electronics', nameSw: 'Elektroniki', icon: '📱', color: 'bg-blue-500', count: 1250 },
  { id: 'fashion', nameEn: 'Fashion', nameSw: 'Mitindo', icon: '👗', color: 'bg-pink-500', count: 3400 },
  { id: 'home', nameEn: 'Home & Living', nameSw: 'Nyumbani', icon: '🏠', color: 'bg-amber-500', count: 890 },
  { id: 'beauty', nameEn: 'Beauty & Health', nameSw: 'Urembo na Afya', icon: '💄', color: 'bg-purple-500', count: 670 },
  { id: 'food', nameEn: 'Food & Groceries', nameSw: 'Chakula', icon: '🍎', color: 'bg-green-500', count: 2100 },
  { id: 'sports', nameEn: 'Sports', nameSw: 'Michezo', icon: '⚽', color: 'bg-red-500', count: 540 },
  { id: 'books', nameEn: 'Books & Media', nameSw: 'Vitabu', icon: '📚', color: 'bg-indigo-500', count: 780 },
  { id: 'toys', nameEn: 'Toys & Kids', nameSw: 'Watoto', icon: '🧸', color: 'bg-yellow-500', count: 920 },
]

export default function CategoriesPage() {
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8">
          {isSwahili ? 'Kategoria Zote' : 'All Categories'}
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category) => (
            <Link
              key={category.id}
              href={`/categories/${category.id}`}
              className="card p-8 hover:scale-105 transition-transform cursor-pointer"
            >
              <div className={`${category.color} w-20 h-20 rounded-full flex items-center justify-center text-4xl mx-auto mb-4`}>
                {category.icon}
              </div>
              <h2 className="text-xl font-bold text-gray-900 text-center mb-2">
                {isSwahili ? category.nameSw : category.nameEn}
              </h2>
              <p className="text-gray-600 text-center text-sm">
                {category.count.toLocaleString()} {isSwahili ? 'bidhaa' : 'products'}
              </p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}

