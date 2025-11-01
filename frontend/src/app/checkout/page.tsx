'use client'

import { useState } from 'react'
import { useCartStore } from '@/store/cartStore'
import { useUserStore } from '@/store/userStore'
import { useLanguageStore } from '@/store/languageStore'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import axios from 'axios'

export default function CheckoutPage() {
  const { items, getTotalPrice, clearCart } = useCartStore()
  const { user } = useUserStore()
  const { language } = useLanguageStore()
  const router = useRouter()
  const isSwahili = language === 'sw'

  const [formData, setFormData] = useState({
    fullName: (user as any)?.full_name || user?.name || '',
    email: user?.email || '',
    phone: '',
    county: 'Nairobi',
    address: '',
    paymentMethod: 'mpesa'
  })

  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (items.length === 0) {
      toast.error(isSwahili ? 'Kikapu kipo tupu' : 'Cart is empty')
      return
    }

    setLoading(true)

    try {
      const orderData = {
        user_id: user?.id || 'guest',
        items: items.map(item => ({
          product_id: item.id,
          name: item.name,
          quantity: item.quantity,
          price: item.price
        })),
        total_amount: getTotalPrice(),
        customer_details: formData,
        payment_method: formData.paymentMethod
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await axios.post(`${API_URL}/api/v1/orders`, orderData)

      if (response.data.success) {
        // Check if demo mode
        const isDemoMode = response.data.mpesa_instructions?.demo_mode
        
        if (isDemoMode) {
          toast.success(
            isSwahili 
              ? '🎉 Agizo limefanikiwa! (Hali ya Majaribio)' 
              : '🎉 Order placed successfully! (Demo Mode)',
            { duration: 4000 }
          )
        } else {
          toast.success(isSwahili ? 'Agizo limefanikiwa!' : 'Order placed successfully!')
        }
        
        clearCart()
        router.push(`/orders/${response.data.order_id}`)
      }
    } catch (error) {
      console.error('Order failed:', error)
      toast.error(isSwahili ? 'Agizo limeshindwa' : 'Order failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (items.length === 0) {
    router.push('/cart')
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          {isSwahili ? 'Maliza Ununuzi' : 'Checkout'}
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Checkout Form */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Customer Information */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-bold mb-4">
                  {isSwahili ? 'Maelezo ya Mteja' : 'Customer Information'}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {isSwahili ? 'Jina Kamili' : 'Full Name'} *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.fullName}
                      onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                      className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {isSwahili ? 'Barua pepe' : 'Email'} *
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {isSwahili ? 'Nambari ya Simu' : 'Phone Number'} *
                    </label>
                    <input
                      type="tel"
                      required
                      placeholder="254712345678"
                      value={formData.phone}
                      onChange={(e) => setFormData({...formData, phone: e.target.value})}
                      className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {isSwahili ? 'Kaunti' : 'County'} *
                    </label>
                    <select
                      value={formData.county}
                      onChange={(e) => setFormData({...formData, county: e.target.value})}
                      className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                    >
                      <option value="Nairobi">Nairobi</option>
                      <option value="Mombasa">Mombasa</option>
                      <option value="Kisumu">Kisumu</option>
                      <option value="Nakuru">Nakuru</option>
                      <option value="Kiambu">Kiambu</option>
                    </select>
                  </div>
                </div>
                <div className="mt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {isSwahili ? 'Anwani ya Kutolea' : 'Delivery Address'} *
                  </label>
                  <textarea
                    required
                    rows={3}
                    value={formData.address}
                    onChange={(e) => setFormData({...formData, address: e.target.value})}
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                    placeholder={isSwahili ? 'Ingiza anwani kamili' : 'Enter full address'}
                  />
                </div>
              </div>

              {/* Payment Method */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-bold mb-4">
                  {isSwahili ? 'Njia ya Malipo' : 'Payment Method'}
                </h2>
                <div className="space-y-3">
                  <label className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      name="payment"
                      value="mpesa"
                      checked={formData.paymentMethod === 'mpesa'}
                      onChange={(e) => setFormData({...formData, paymentMethod: e.target.value})}
                      className="mr-3"
                    />
                    <div className="flex-1">
                      <span className="font-semibold">M-Pesa</span>
                      <p className="text-sm text-gray-600">
                        {isSwahili ? 'Lipia kwa M-Pesa' : 'Pay via M-Pesa'}
                      </p>
                    </div>
                    <span className="text-2xl">📱</span>
                  </label>
                  <label className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      name="payment"
                      value="cash"
                      checked={formData.paymentMethod === 'cash'}
                      onChange={(e) => setFormData({...formData, paymentMethod: e.target.value})}
                      className="mr-3"
                    />
                    <div className="flex-1">
                      <span className="font-semibold">
                        {isSwahili ? 'Pesa Taslimu' : 'Cash on Delivery'}
                      </span>
                      <p className="text-sm text-gray-600">
                        {isSwahili ? 'Lipia wakati wa kutolea' : 'Pay when you receive'}
                      </p>
                    </div>
                    <span className="text-2xl">💵</span>
                  </label>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-green-600 text-white py-4 rounded-lg hover:bg-green-700 font-semibold text-lg transition-colors disabled:bg-gray-400"
              >
                {loading 
                  ? (isSwahili ? 'Inatuma...' : 'Placing Order...') 
                  : (isSwahili ? 'Weka Agizo' : 'Place Order')}
              </button>
            </form>
          </div>

          {/* Order Summary */}
          <div>
            <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
              <h2 className="text-xl font-bold mb-4">
                {isSwahili ? 'Muhtasari wa Agizo' : 'Order Summary'}
              </h2>
              <div className="space-y-3 mb-4 max-h-64 overflow-y-auto">
                {items.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      {item.name} x {item.quantity}
                    </span>
                    <span className="font-semibold">
                      KES {(item.price * item.quantity).toLocaleString()}
                    </span>
                  </div>
                ))}
              </div>
              <div className="border-t pt-4 space-y-2">
                <div className="flex justify-between text-gray-600">
                  <span>{isSwahili ? 'Bei ya Vitu' : 'Subtotal'}</span>
                  <span>KES {getTotalPrice().toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>{isSwahili ? 'Usafirishaji' : 'Delivery'}</span>
                  <span>{isSwahili ? 'Bure' : 'Free'}</span>
                </div>
                <div className="border-t pt-2 flex justify-between text-xl font-bold">
                  <span>{isSwahili ? 'Jumla' : 'Total'}</span>
                  <span className="text-green-600">KES {getTotalPrice().toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
