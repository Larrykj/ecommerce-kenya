'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function AdminDashboard() {
  const router = useRouter()
  const [stats, setStats] = useState({
    totalProducts: 15,
    totalOrders: 0,
    totalRevenue: 0,
    totalUsers: 2,
    pendingOrders: 0,
    lowStock: 3
  })

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
            <div className="flex items-center gap-4">
              <button className="text-gray-600 hover:text-gray-900">
                🔔 Notifications
              </button>
              <button 
                onClick={() => router.push('/')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Store
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Products</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalProducts}</p>
              </div>
              <div className="text-4xl">📦</div>
            </div>
            <Link href="/admin/products" className="text-sm text-green-600 hover:text-green-700 mt-2 inline-block">
              Manage Products →
            </Link>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Orders</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalOrders}</p>
              </div>
              <div className="text-4xl">🛒</div>
            </div>
            <Link href="/admin/orders" className="text-sm text-green-600 hover:text-green-700 mt-2 inline-block">
              View Orders →
            </Link>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Revenue</p>
                <p className="text-3xl font-bold text-gray-900">KES {stats.totalRevenue.toLocaleString()}</p>
              </div>
              <div className="text-4xl">💰</div>
            </div>
            <p className="text-sm text-gray-500 mt-2">This month</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Users</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalUsers}</p>
              </div>
              <div className="text-4xl">👥</div>
            </div>
            <Link href="/admin/users" className="text-sm text-green-600 hover:text-green-700 mt-2 inline-block">
              Manage Users →
            </Link>
          </div>
        </div>

        {/* Alerts */}
        {stats.lowStock > 0 && (
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <span className="text-2xl">⚠️</span>
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-700">
                  <span className="font-medium">{stats.lowStock} products</span> are low in stock. 
                  <Link href="/admin/products" className="font-medium underline ml-1">
                    View inventory
                  </Link>
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Orders */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Recent Orders</h2>
            </div>
            <div className="p-6">
              <div className="text-center py-8 text-gray-500">
                <p className="text-4xl mb-2">📋</p>
                <p>No orders yet</p>
                <p className="text-sm mt-1">Orders will appear here when customers make purchases</p>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Quick Actions</h2>
            </div>
            <div className="p-6 space-y-3">
              <Link 
                href="/admin/products/new"
                className="block w-full bg-green-600 text-white text-center py-3 rounded-lg hover:bg-green-700 font-semibold"
              >
                ➕ Add New Product
              </Link>
              <Link 
                href="/admin/orders"
                className="block w-full border-2 border-gray-300 text-gray-700 text-center py-3 rounded-lg hover:bg-gray-50 font-semibold"
              >
                📦 Process Orders
              </Link>
              <Link 
                href="/admin/analytics"
                className="block w-full border-2 border-gray-300 text-gray-700 text-center py-3 rounded-lg hover:bg-gray-50 font-semibold"
              >
                📊 View Analytics
              </Link>
              <Link 
                href="/admin/settings"
                className="block w-full border-2 border-gray-300 text-gray-700 text-center py-3 rounded-lg hover:bg-gray-50 font-semibold"
              >
                ⚙️ Settings
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
