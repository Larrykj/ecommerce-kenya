'use client'

import { useParams, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { useCartStore } from '@/store/cartStore'
import { useLanguageStore } from '@/store/languageStore'
import axios from 'axios'
import toast from 'react-hot-toast'

interface Product {
  id: string
  name: string
  name_sw?: string
  description: string
  description_sw?: string
  price: number
  original_price?: number
  discount_percentage?: number
  images: string[]
  category: string
  rating?: number
  review_count?: number
  stock: number
  vendor_name?: string
  county?: string
  tags?: string[]
}

export default function ProductDetailPage() {
  const params = useParams()
  const router = useRouter()
  const { language } = useLanguageStore()
  const { addItem } = useCartStore()
  const isSwahili = language === 'sw'
  
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [quantity, setQuantity] = useState(1)
  const [selectedImage, setSelectedImage] = useState(0)

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${API_URL}/api/v1/products/${params.id}`)
        setProduct(response.data)
      } catch (error) {
        console.error('Failed to fetch product:', error)
        toast.error(isSwahili ? 'Bidhaa haijapatikana' : 'Product not found')
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchProduct()
    }
  }, [params.id, isSwahili])

  const handleAddToCart = () => {
    if (product) {
      addItem({
        id: product.id,
        name: product.name,
        price: product.price,
        quantity: quantity,
        image: product.images[0]
      })
      toast.success(
        isSwahili ? `${quantity} imeongezwa kwenye kikapu` : `${quantity} added to cart`,
        { icon: '🛒' }
      )
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{isSwahili ? 'Inapakia...' : 'Loading...'}</p>
        </div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {isSwahili ? 'Bidhaa haijapatikana' : 'Product not found'}
          </h1>
          <button onClick={() => router.push('/')} className="btn-primary">
            {isSwahili ? 'Rudi Nyumbani' : 'Go Home'}
          </button>
        </div>
      </div>
    )
  }

  const displayName = isSwahili && product.name_sw ? product.name_sw : product.name
  const displayDescription = isSwahili && product.description_sw ? product.description_sw : product.description

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8 text-sm">
          <a href="/" className="text-gray-600 hover:text-green-600">
            {isSwahili ? 'Nyumbani' : 'Home'}
          </a>
          <span className="mx-2 text-gray-400">/</span>
          <a href="/categories" className="text-gray-600 hover:text-green-600">
            {isSwahili ? 'Kategoria' : 'Categories'}
          </a>
          <span className="mx-2 text-gray-400">/</span>
          <span className="text-gray-900">{displayName}</span>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Images */}
          <div>
            <div className="bg-white rounded-lg shadow-md overflow-hidden mb-4">
              <img
                src={product.images[selectedImage] || product.images[0]}
                alt={displayName}
                className="w-full h-96 object-cover"
              />
            </div>
            {product.images.length > 1 && (
              <div className="grid grid-cols-4 gap-2">
                {product.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={`border-2 rounded-lg overflow-hidden ${
                      selectedImage === index ? 'border-green-600' : 'border-gray-200'
                    }`}
                  >
                    <img src={image} alt={`${displayName} ${index + 1}`} className="w-full h-20 object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{displayName}</h1>

            {/* Rating */}
            {product.rating && (
              <div className="flex items-center mb-4">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className={i < Math.round(product.rating!) ? 'text-yellow-400' : 'text-gray-300'}>
                      ★
                    </span>
                  ))}
                </div>
                <span className="ml-2 text-gray-600">
                  {product.rating.toFixed(1)} ({product.review_count} {isSwahili ? 'mapitio' : 'reviews'})
                </span>
              </div>
            )}

            {/* Price */}
            <div className="mb-6">
              <div className="flex items-baseline gap-3">
                <span className="text-3xl font-bold text-green-600">
                  KES {product.price.toLocaleString()}
                </span>
                {product.original_price && product.original_price > product.price && (
                  <>
                    <span className="text-xl text-gray-400 line-through">
                      KES {product.original_price.toLocaleString()}
                    </span>
                    {product.discount_percentage && (
                      <span className="bg-red-500 text-white px-2 py-1 rounded text-sm font-bold">
                        -{product.discount_percentage}%
                      </span>
                    )}
                  </>
                )}
              </div>
            </div>

            {/* Description */}
            <div className="mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                {isSwahili ? 'Maelezo' : 'Description'}
              </h2>
              <p className="text-gray-700 leading-relaxed">{displayDescription}</p>
            </div>

            {/* Vendor Info */}
            {product.vendor_name && (
              <div className="bg-gray-100 rounded-lg p-4 mb-6">
                <p className="text-sm text-gray-600">
                  {isSwahili ? 'Mchuzaji' : 'Seller'}: <span className="font-semibold text-gray-900">{product.vendor_name}</span>
                </p>
                {product.county && (
                  <p className="text-sm text-gray-600">
                    {isSwahili ? 'Eneo' : 'Location'}: <span className="font-semibold text-gray-900">{product.county}</span>
                  </p>
                )}
              </div>
            )}

            {/* Stock Status */}
            <div className="mb-6">
              {product.stock > 0 ? (
                <p className="text-green-600 font-semibold">
                  ✓ {isSwahili ? 'Inapatikana' : 'In Stock'} ({product.stock} {isSwahili ? 'vitu' : 'items'})
                </p>
              ) : (
                <p className="text-red-600 font-semibold">
                  {isSwahili ? 'Hazipatikani' : 'Out of Stock'}
                </p>
              )}
            </div>

            {/* Quantity Selector */}
            {product.stock > 0 && (
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {isSwahili ? 'Idadi' : 'Quantity'}
                </label>
                <div className="flex items-center gap-4">
                  <div className="flex items-center border rounded-lg">
                    <button
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="px-4 py-2 hover:bg-gray-100"
                    >
                      -
                    </button>
                    <span className="px-6 py-2 border-x">{quantity}</span>
                    <button
                      onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                      className="px-4 py-2 hover:bg-gray-100"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Add to Cart Button */}
            <div className="flex gap-4">
              <button
                onClick={handleAddToCart}
                disabled={product.stock === 0}
                className="flex-1 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 font-semibold disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isSwahili ? 'Ongeza kwenye Kikapu' : 'Add to Cart'}
              </button>
              <button
                onClick={() => {
                  handleAddToCart()
                  router.push('/cart')
                }}
                disabled={product.stock === 0}
                className="flex-1 border-2 border-green-600 text-green-600 py-3 rounded-lg hover:bg-green-50 font-semibold disabled:border-gray-400 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isSwahili ? 'Nunua Sasa' : 'Buy Now'}
              </button>
            </div>

            {/* Tags */}
            {product.tags && product.tags.length > 0 && (
              <div className="mt-6">
                <div className="flex flex-wrap gap-2">
                  {product.tags.map((tag, index) => (
                    <span key={index} className="bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-sm">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
