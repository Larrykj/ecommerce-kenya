'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import toast from 'react-hot-toast'

export default function NewProductPage() {
  const router = useRouter()
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate
    if (!formData.name || !formData.description || formData.price <= 0) {
      toast.error('Please fill in all required fields')
      return
    }

    // Demo success
    toast.success('Product added successfully! (Demo - no backend save)')
    router.push('/admin/products')
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href="/admin/products" className="text-sm text-gray-600 hover:text-gray-900">
            ← Back to Products
          </Link>
          <h1 className="text-2xl font-bold text-gray-900 mt-1">Add New Product</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-6">
          
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
              placeholder="e.g., Samsung Galaxy S24"
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
              placeholder="e.g., Samsung Galaxy S24"
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
              placeholder="Describe the product features..."
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
              placeholder="Eleza sifa za bidhaa..."
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
                placeholder="0.00"
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
                placeholder="0"
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
            <p className="text-sm text-gray-500 mt-1">
              Use Unsplash URLs or upload to CDN
            </p>
            {formData.images[0] && (
              <img 
                src={formData.images[0]} 
                alt="Preview" 
                className="mt-2 h-32 w-32 object-cover rounded"
                onError={(e) => {
                  e.currentTarget.style.display = 'none'
                }}
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
              Add Product
            </button>
          </div>

          {/* Note */}
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
            <p className="text-sm text-blue-700">
              <strong>Note:</strong> This is a demo form. In production, this would call a POST endpoint 
              to create a new product in the database.
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}
