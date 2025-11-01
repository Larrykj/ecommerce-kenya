'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { FiShoppingCart, FiUser, FiSearch, FiMenu, FiGlobe, FiLogIn, FiLogOut } from 'react-icons/fi'
import { useCartStore } from '@/store/cartStore'
import { useLanguageStore } from '@/store/languageStore'
import { useUserStore } from '@/store/userStore'

export default function Header() {
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState('')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { items } = useCartStore()
  const { language, toggleLanguage } = useLanguageStore()
  const { user, logout } = useUserStore()
  
  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (!token && user) {
      logout()
    }
  }, [user, logout])
  
  const cartItemCount = items.reduce((sum, item) => sum + item.quantity, 0)

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    logout()
    router.push('/')
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Navigate to search results
    window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`
  }

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top Bar */}
        <div className="flex items-center justify-between py-4">
          
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">SK</span>
            </div>
            <div className="hidden sm:block">
              <h1 className="text-2xl font-bold text-gray-900">Shop<span className="text-primary-600">KE</span></h1>
              <p className="text-xs text-gray-500">
                {language === 'en' ? 'Shop Smart, Shop Local' : 'Nunua Kwa Akili, Nunua Hapa'}
              </p>
            </div>
          </Link>

          {/* Search Bar - Desktop */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-2xl mx-8">
            <div className="relative w-full">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={language === 'en' ? 'Search products...' : 'Tafuta bidhaa...'}
                className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <button type="submit" className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-primary-600">
                <FiSearch size={20} />
              </button>
            </div>
          </form>

          {/* Right Actions */}
          <div className="flex items-center space-x-4">
            {/* Language Toggle */}
            <button
              onClick={toggleLanguage}
              className="hidden sm:flex items-center space-x-1 text-gray-600 hover:text-primary-600"
              title={language === 'en' ? 'Switch to Swahili' : 'Badili kwa Kiingereza'}
            >
              <FiGlobe size={20} />
              <span className="text-sm font-medium">{language === 'en' ? 'SW' : 'EN'}</span>
            </button>

            {/* Cart */}
            <Link href="/cart" className="relative text-gray-600 hover:text-primary-600">
              <FiShoppingCart size={24} />
              {cartItemCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-primary-600 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                  {cartItemCount}
                </span>
              )}
            </Link>

            {/* User Account / Login */}
            {user ? (
              <>
                <Link href="/account" className="text-gray-600 hover:text-primary-600" title={user.name || user.email}>
                  <FiUser size={24} />
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-600 hover:text-primary-600"
                  title="Logout"
                >
                  <FiLogOut size={20} />
                </button>
              </>
            ) : (
              <Link href="/login" className="text-gray-600 hover:text-primary-600" title="Login">
                <FiLogIn size={24} />
              </Link>
            )}

            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-gray-600 hover:text-primary-600"
            >
              <FiMenu size={24} />
            </button>
          </div>
        </div>

        {/* Mobile Search */}
        <form onSubmit={handleSearch} className="md:hidden pb-4">
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={language === 'en' ? 'Search products...' : 'Tafuta bidhaa...'}
              className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <button type="submit" className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
              <FiSearch size={20} />
            </button>
          </div>
        </form>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center space-x-8 pb-4 border-t border-gray-200 pt-4">
          <Link href="/categories" className="text-gray-700 hover:text-primary-600 font-medium">
            {language === 'en' ? 'Categories' : 'Kategoria'}
          </Link>
          <Link href="/trending" className="text-gray-700 hover:text-primary-600 font-medium">
            {language === 'en' ? 'Trending' : 'Vya Kawaida'}
          </Link>
          <Link href="/local-vendors" className="text-gray-700 hover:text-primary-600 font-medium">
            {language === 'en' ? 'Local Vendors' : 'Wafanyabiashara wa Ndani'}
          </Link>
          <Link href="/deals" className="text-gray-700 hover:text-primary-600 font-medium">
            {language === 'en' ? 'Deals' : 'Ofa'}
          </Link>
        </nav>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden pb-4 space-y-2">
            <Link href="/categories" className="block py-2 text-gray-700 hover:text-primary-600 font-medium">
              {language === 'en' ? 'Categories' : 'Kategoria'}
            </Link>
            <Link href="/trending" className="block py-2 text-gray-700 hover:text-primary-600 font-medium">
              {language === 'en' ? 'Trending' : 'Vya Kawaida'}
            </Link>
            <Link href="/local-vendors" className="block py-2 text-gray-700 hover:text-primary-600 font-medium">
              {language === 'en' ? 'Local Vendors' : 'Wafanyabiashara wa Ndani'}
            </Link>
            <Link href="/deals" className="block py-2 text-gray-700 hover:text-primary-600 font-medium">
              {language === 'en' ? 'Deals' : 'Ofa'}
            </Link>
            <button
              onClick={toggleLanguage}
              className="block py-2 text-gray-700 hover:text-primary-600 font-medium w-full text-left"
            >
              <FiGlobe className="inline mr-2" />
              {language === 'en' ? 'Badili kwa Kiswahili' : 'Switch to English'}
            </button>
          </nav>
        )}
      </div>
    </header>
  )
}

