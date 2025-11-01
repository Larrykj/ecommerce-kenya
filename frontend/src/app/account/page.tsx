'use client'

import { useLanguageStore } from '@/store/languageStore'
import { useUserStore } from '@/store/userStore'

export default function AccountPage() {
  const { language } = useLanguageStore()
  const { user } = useUserStore()
  const isSwahili = language === 'sw'

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          {isSwahili ? 'Akaunti Yangu' : 'My Account'}
        </h1>

        <div className="bg-white rounded-lg shadow-md p-8">
          {user ? (
            <div>
              <p className="text-lg">{isSwahili ? 'Karibu,' : 'Welcome,'} {user.name || 'User'}!</p>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-6">
                {isSwahili ? 'Ingia ili kuona akaunti yako' : 'Sign in to view your account'}
              </p>
              <button className="btn-primary">
                {isSwahili ? 'Ingia' : 'Sign In'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

