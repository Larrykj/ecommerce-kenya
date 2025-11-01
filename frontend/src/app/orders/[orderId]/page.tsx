'use client'

import { useParams, useRouter } from 'next/navigation'
import { useLanguageStore } from '@/store/languageStore'

export default function OrderConfirmationPage() {
  const params = useParams()
  const router = useRouter()
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'
  const orderId = params.orderId as string

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Success Message */}
        <div className="bg-white rounded-lg shadow-md p-8 text-center mb-6">
          <div className="text-6xl mb-4">✅</div>
          <h1 className="text-3xl font-bold text-green-600 mb-2">
            {isSwahili ? 'Agizo Limefanikiwa!' : 'Order Successful!'}
          </h1>
          <p className="text-gray-600 mb-4">
            {isSwahili 
              ? 'Asante kwa ununuzi wako. Agizo lako limepokewa.' 
              : 'Thank you for your purchase. Your order has been received.'}
          </p>
          <div className="bg-gray-100 rounded-lg p-4 inline-block">
            <p className="text-sm text-gray-600">{isSwahili ? 'Nambari ya Agizo' : 'Order Number'}</p>
            <p className="text-2xl font-bold text-gray-900">{orderId}</p>
          </div>
        </div>

        {/* Order Details */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">
            {isSwahili ? 'Maelezo ya Agizo' : 'Order Details'}
          </h2>
          <div className="space-y-3">
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">{isSwahili ? 'Hali' : 'Status'}</span>
              <span className="font-semibold text-yellow-600">
                {isSwahili ? 'Inasubiri' : 'Pending'}
              </span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">{isSwahili ? 'Hali ya Malipo' : 'Payment Status'}</span>
              <span className="font-semibold text-yellow-600">
                {isSwahili ? 'Inasubiri' : 'Pending'}
              </span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">{isSwahili ? 'Muda wa Kutolea' : 'Estimated Delivery'}</span>
              <span className="font-semibold">2-3 {isSwahili ? 'siku za kazi' : 'business days'}</span>
            </div>
          </div>
        </div>

        {/* M-Pesa Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <div className="flex items-start gap-3">
            <span className="text-3xl">📱</span>
            <div>
              <h3 className="font-bold text-blue-900 mb-2">
                {isSwahili ? 'Maelekezo ya M-Pesa' : 'M-Pesa Instructions'}
              </h3>
              <p className="text-blue-800 text-sm">
                {isSwahili 
                  ? 'Utapokea ujumbe wa M-Pesa kwenye simu yako. Ingiza PIN yako ili kukamilisha malipo.'
                  : 'You will receive an M-Pesa prompt on your phone. Enter your PIN to complete the payment.'}
              </p>
            </div>
          </div>
        </div>

        {/* Next Steps */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">
            {isSwahili ? 'Hatua Zinazofuata' : 'What\'s Next?'}
          </h2>
          <ol className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="bg-green-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold flex-shrink-0">1</span>
              <p className="text-gray-700">
                {isSwahili 
                  ? 'Lipia kwa M-Pesa kupitia ujumbe utakaofikia'
                  : 'Complete payment via M-Pesa prompt'}
              </p>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-green-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold flex-shrink-0">2</span>
              <p className="text-gray-700">
                {isSwahili 
                  ? 'Utapokea barua pepe ya uthibitisho'
                  : 'You\'ll receive a confirmation email'}
              </p>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-green-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold flex-shrink-0">3</span>
              <p className="text-gray-700">
                {isSwahili 
                  ? 'Agizo lako litaandaliwa na kutumwa'
                  : 'Your order will be prepared and shipped'}
              </p>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-green-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold flex-shrink-0">4</span>
              <p className="text-gray-700">
                {isSwahili 
                  ? 'Utapokea agizo lako ndani ya siku 2-3 za kazi'
                  : 'Receive your order within 2-3 business days'}
              </p>
            </li>
          </ol>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={() => router.push('/')}
            className="flex-1 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 font-semibold transition-colors"
          >
            {isSwahili ? 'Endelea Kununua' : 'Continue Shopping'}
          </button>
          <button
            onClick={() => router.push('/account')}
            className="flex-1 border border-gray-300 py-3 rounded-lg hover:bg-gray-50 transition-colors"
          >
            {isSwahili ? 'Angalia Maagizo Yangu' : 'View My Orders'}
          </button>
        </div>
      </div>
    </div>
  )
}
