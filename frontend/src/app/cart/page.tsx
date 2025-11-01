'use client'

import { useCartStore } from '@/store/cartStore'
import { useLanguageStore } from '@/store/languageStore'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'

export default function CartPage() {
  const { items, getTotalPrice, getTotalItems, removeItem, updateQuantity } = useCartStore()
  const { language } = useLanguageStore()
  const router = useRouter()
  const isSwahili = language === 'sw'

  const handleCheckout = () => {
    if (items.length === 0) {
      toast.error(isSwahili ? 'Kikapu kipo tupu' : 'Cart is empty')
      return
    }
    router.push('/checkout')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          {isSwahili ? 'Kikapu Changu' : 'My Cart'}
        </h1>

        {items.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">🛒</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {isSwahili ? 'Kikapu chako kipo tupu' : 'Your cart is empty'}
            </h2>
            <p className="text-gray-600 mb-6">
              {isSwahili 
                ? 'Anza kununua bidhaa unazozipen da!'
                : 'Start shopping for products you love!'}
            </p>
            <a href="/" className="btn-primary inline-block">
              {isSwahili ? 'Endelea Kununua' : 'Continue Shopping'}
            </a>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-4">
              {items.map((item) => (
                <div key={item.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-center gap-4">
                    {item.image && (
                      <img src={item.image} alt={item.name} className="w-24 h-24 object-cover rounded" />
                    )}
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900">{item.name}</h3>
                      <p className="text-green-600 font-bold mt-1">KES {item.price.toLocaleString()}</p>
                      <div className="flex items-center gap-4 mt-3">
                        <div className="flex items-center border rounded">
                          <button
                            onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
                            className="px-3 py-1 hover:bg-gray-100"
                          >
                            -
                          </button>
                          <span className="px-4 py-1 border-x">{item.quantity}</span>
                          <button
                            onClick={() => updateQuantity(item.id, item.quantity + 1)}
                            className="px-3 py-1 hover:bg-gray-100"
                          >
                            +
                          </button>
                        </div>
                        <button
                          onClick={() => {
                            removeItem(item.id)
                            toast.success(isSwahili ? 'Imeondolewa' : 'Removed from cart')
                          }}
                          className="text-red-600 hover:text-red-700 text-sm"
                        >
                          {isSwahili ? 'Ondoa' : 'Remove'}
                        </button>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-gray-900">
                        KES {(item.price * item.quantity).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div>
              <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
                <h2 className="text-xl font-bold mb-4">
                  {isSwahili ? 'Muhtasari wa Malipo' : 'Order Summary'}
                </h2>
                <div className="space-y-3 mb-6">
                  <div className="flex justify-between text-gray-600">
                    <span>{isSwahili ? 'Vitu' : 'Items'} ({getTotalItems()})</span>
                    <span>KES {getTotalPrice().toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-gray-600">
                    <span>{isSwahili ? 'Usafirishaji' : 'Delivery'}</span>
                    <span>{isSwahili ? 'Bure' : 'Free'}</span>
                  </div>
                  <div className="border-t pt-3 flex justify-between text-xl font-bold">
                    <span>{isSwahili ? 'Jumla' : 'Total'}:</span>
                    <span className="text-green-600">KES {getTotalPrice().toLocaleString()}</span>
                  </div>
                </div>
                <button
                  onClick={handleCheckout}
                  className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 font-semibold transition-colors"
                >
                  {isSwahili ? 'Endelea Kulipia' : 'Proceed to Checkout'}
                </button>
                <button
                  onClick={() => router.push('/')}
                  className="w-full mt-3 border border-gray-300 py-3 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  {isSwahili ? 'Endelea Kununua' : 'Continue Shopping'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

