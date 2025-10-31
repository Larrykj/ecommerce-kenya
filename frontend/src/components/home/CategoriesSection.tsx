'use client'

import Link from 'next/link'
import { useLanguageStore } from '@/store/languageStore'

const categories = [
  { id: 'electronics', nameEn: 'Electronics', nameSw: 'Elektroniki', icon: '📱', color: 'bg-blue-500' },
  { id: 'fashion', nameEn: 'Fashion', nameSw: 'Mitindo', icon: '👗', color: 'bg-pink-500' },
  { id: 'home', nameEn: 'Home & Living', nameSw: 'Nyumbani', icon: '🏠', color: 'bg-amber-500' },
  { id: 'beauty', nameEn: 'Beauty & Health', nameSw: 'Urembo na Afya', icon: '💄', color: 'bg-purple-500' },
  { id: 'food', nameEn: 'Food & Groceries', nameSw: 'Chakula', icon: '🍎', color: 'bg-green-500' },
  { id: 'sports', nameEn: 'Sports', nameSw: 'Michezo', icon: '⚽', color: 'bg-red-500' },
  { id: 'books', nameEn: 'Books & Media', nameSw: 'Vitabu', icon: '📚', color: 'bg-indigo-500' },
  { id: 'toys', nameEn: 'Toys & Kids', nameSw: 'Watoto', icon: '🧸', color: 'bg-yellow-500' },
]

export default function CategoriesSection() {
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'

  return (
    <section>
      <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6">
        {isSwahili ? 'Tafuta kwa Kategoria' : 'Shop by Category'}
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        {categories.map((category) => (
          <Link
            key={category.id}
            href={`/categories/${category.id}`}
            className="card p-6 hover:scale-105 transition-transform cursor-pointer text-center"
          >
            <div className={`${category.color} w-16 h-16 rounded-full flex items-center justify-center text-3xl mx-auto mb-3`}>
              {category.icon}
            </div>
            <p className="font-semibold text-sm text-gray-800">
              {isSwahili ? category.nameSw : category.nameEn}
            </p>
          </Link>
        ))}
      </div>
    </section>
  )
}

