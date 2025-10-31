'use client'

import Link from 'next/link'
import { FiShoppingCart, FiHeart } from 'react-icons/fi'
import { useCartStore } from '@/store/cartStore'
import { useLanguageStore } from '@/store/languageStore'
import toast from 'react-hot-toast'

interface Product {
  id: string
  name: string
  name_sw?: string
  price: number
  original_price?: number
  discount_percentage?: number
  image?: string
  average_rating?: number
  is_local_vendor?: boolean
}

interface ProductCardProps {
  product: Product
}

export default function ProductCard({ product }: ProductCardProps) {
  const { addItem } = useCartStore()
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault()
    addItem({
      id: product.id,
      name: product.name,
      price: product.price,
      quantity: 1,
      image: product.image
    })
    toast.success(
      isSwahili ? 'Imeongezwa kwenye kikapu' : 'Added to cart',
      { icon: '🛒' }
    )
  }

  const displayName = isSwahili && product.name_sw ? product.name_sw : product.name

  return (
    <Link href={`/products/${product.id}`} className="card overflow-hidden group">
      {/* Image */}
      <div className="relative aspect-square bg-gray-100">
        {product.image ? (
          <img 
            src={product.image} 
            alt={displayName}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-4xl">
            📦
          </div>
        )}
        
        {/* Badges */}
        <div className="absolute top-2 left-2 space-y-1">
          {product.discount_percentage && product.discount_percentage > 0 && (
            <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
              -{product.discount_percentage}%
            </span>
          )}
          {product.is_local_vendor && (
            <span className="block bg-kenyan-green text-white text-xs font-bold px-2 py-1 rounded">
              🇰🇪 {isSwahili ? 'Ndani' : 'Local'}
            </span>
          )}
        </div>

        {/* Wishlist Button */}
        <button 
          className="absolute top-2 right-2 bg-white p-2 rounded-full shadow-md hover:bg-gray-100 opacity-0 group-hover:opacity-100 transition-opacity"
          onClick={(e) => {
            e.preventDefault()
            toast.success(isSwahili ? 'Imeongezwa kwenye orodha ya matakwa' : 'Added to wishlist')
          }}
        >
          <FiHeart size={18} />
        </button>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 text-sm">
          {displayName}
        </h3>

        {/* Rating */}
        {product.average_rating && (
          <div className="flex items-center text-xs text-gray-600 mb-2">
            <span className="text-yellow-400">★</span>
            <span className="ml-1">{product.average_rating.toFixed(1)}</span>
          </div>
        )}

        {/* Price */}
        <div className="flex items-baseline gap-2 mb-3">
          <span className="text-lg font-bold text-gray-900">
            KES {product.price.toLocaleString()}
          </span>
          {product.original_price && product.original_price > product.price && (
            <span className="text-sm text-gray-400 line-through">
              {product.original_price.toLocaleString()}
            </span>
          )}
        </div>

        {/* Add to Cart Button */}
        <button
          onClick={handleAddToCart}
          className="w-full btn-primary text-sm py-2 flex items-center justify-center gap-2"
        >
          <FiShoppingCart size={16} />
          {isSwahili ? 'Ongeza' : 'Add to Cart'}
        </button>
      </div>
    </Link>
  )
}

