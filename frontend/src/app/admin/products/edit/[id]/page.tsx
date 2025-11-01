'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import axios from 'axios'
import Link from 'next/link'
import toast from 'react-hot-toast'

export default function EditProductPage() {
  const params = useParams()
  const router = useRouter()
  const productId = params.id as string

  const [loading, setLoading] = useState(true)
  const [formData, setFormData] = useState({
    name: '',
    name_sw: '',
    description: '',
    description_sw: '',
    price: 0,
    stock: 0,
    category: 'electronics',
    images: ['']
  })

  useEffect(() => {
    fetchProduct()
  }, [productId])

  const fetchProduct = async () => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await axios.get(`${API_URL}/api/v1/products/${productId}`)
      const product = response.data
      
      setFormData({
        name: product.name || '',
        name_sw: product.name_sw || '',
        description: product.description || '',
        description_sw: product.description_sw || '',
        price: product.price || 0,
        stock: product.stock_quantity || 0,
        category: product.category || 'electronics',
        images: product.images || ['']
      })
    } catch (error) {
      console.error('Failed to fetch product:', error)
      toast.error('Failed to load product')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    toast.success('Product updated successfully! (Demo - no backend update)')
    router.push('/admin/products')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href="/admin/products" className="text-sm text-gray-600 hover:text-gray-900">
            ← Back to Products
          </Link>
          <h1 className="text-2xl font-bold text-gray-900 mt-1">Edit Product</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-6">
          
          {/* Product ID (Read-only) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Product ID</label>
            <input
              type="text"
              value={productId}
              disabled
              className="w-full px-4 py-2 border rounded-lg bg-gray-100 text-gray-600"
            />
          </div>

          {/* Product Name (English) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Name (English) *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Product Name (Swahili) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Name (Swahili)
            </label>
            <input
              type="text"
              value={formData.name_sw}
              onChange={(e) => setFormData({...formData, name_sw: e.target.value})}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Description (English) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description (English) *
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              required
              rows={3}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Description (Swahili) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description (Swahili)
            </label>
            <textarea
              value={formData.description_sw}
              onChange={(e) => setFormData({...formData, description_sw: e.target.value})}
              rows={3}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
            />
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Category *</label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
            >
              <option value="electronics">Electronics</option>
              <option value="fashion">Fashion</option>
              <option value="home">Home & Living</option>
              <option value="beauty">Beauty & Health</option>
              <option value="food">Food & Groceries</option>
              <option value="sports">Sports</option>
            </select>
          </div>

          {/* Price and Stock */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Price (KES) *</label>
              <input
                type="number"
                value={formData.price}
                onChange={(e) => setFormData({...formData, price: parseFloat(e.target.value)})}
                required
                min="0"
                step="0.01"
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Stock Quantity *</label>
              <input
                type="number"
                value={formData.stock}
                onChange={(e) => setFormData({...formData, stock: parseInt(e.target.value)})}
                required
                min="0"
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
              />
            </div>
          </div>

          {/* Image URL */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Image URL
            </label>
            <input
              type="url"
              value={formData.images[0]}
              onChange={(e) => setFormData({...formData, images: [e.target.value]})}
              placeholder="https://images.unsplash.com/photo-..."
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
            />
            {formData.images[0] && (
              <img 
                src={formData.images[0]} 
                alt="Preview" 
                className="mt-2 h-32 w-32 object-cover rounded"
              />
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end gap-4 pt-4">
            <Link
              href="/admin/products"
              className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </Link>
            <button
              type="submit"
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold"
            >
              Update Product
            </button>
          </div>

          {/* Note */}
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
            <p className="text-sm text-yellow-700">
              <strong>Note:</strong> This is a demo edit form. Changes are not persisted to the backend. 
              In production, this would call a PUT endpoint to update the product.
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}
