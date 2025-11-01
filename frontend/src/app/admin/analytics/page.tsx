'use client'

import Link from 'next/link'

export default function AdminAnalyticsPage() {
  const salesData = [
    { month: 'Jan', sales: 45000 },
    { month: 'Feb', sales: 52000 },
    { month: 'Mar', sales: 48000 },
    { month: 'Apr', sales: 61000 },
    { month: 'May', sales: 55000 },
    { month: 'Jun', sales: 67000 },
  ]

  const topProducts = [
    { name: 'Samsung Galaxy A54 5G', sales: 45, revenue: 1574955 },
    { name: 'Infinix Note 30 Pro', sales: 32, revenue: 927968 },
    { name: 'JBL Tune 510BT Headphones', sales: 89, revenue: 535911 },
  ]

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href="/admin" className="text-sm text-gray-600 hover:text-gray-900">
            ← Back to Dashboard
          </Link>
          <h1 className="text-2xl font-bold text-gray-900 mt-1">Analytics & Reports</h1>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600">Total Revenue</p>
            <p className="text-3xl font-bold text-gray-900">KES 0</p>
            <p className="text-sm text-green-600 mt-2">+0% from last month</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600">Orders</p>
            <p className="text-3xl font-bold text-gray-900">0</p>
            <p className="text-sm text-green-600 mt-2">+0% from last month</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600">Avg Order Value</p>
            <p className="text-3xl font-bold text-gray-900">KES 0</p>
            <p className="text-sm text-gray-600 mt-2">No change</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-600">Conversion Rate</p>
            <p className="text-3xl font-bold text-gray-900">0%</p>
            <p className="text-sm text-gray-600 mt-2">No data</p>
          </div>
        </div>

        {/* Sales Chart */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Sales Overview (Demo Data)</h2>
          <div className="flex items-end justify-between h-64 gap-4">
            {salesData.map((data, index) => (
              <div key={index} className="flex-1 flex flex-col items-center">
                <div className="w-full bg-green-600 rounded-t" style={{ height: `${(data.sales / 70000) * 100}%` }}></div>
                <p className="text-sm text-gray-600 mt-2">{data.month}</p>
                <p className="text-xs text-gray-500">{(data.sales / 1000).toFixed(0)}K</p>
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Top Products */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Top Products (Demo)</h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {topProducts.map((product, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{product.name}</p>
                      <p className="text-sm text-gray-600">{product.sales} units sold</p>
                    </div>
                    <p className="font-semibold text-gray-900">KES {product.revenue.toLocaleString()}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Regional Sales */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Sales by County (Demo)</h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-900">📍 Nairobi</span>
                  <span className="font-semibold">KES 0</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-900">📍 Mombasa</span>
                  <span className="font-semibold">KES 0</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-900">📍 Kisumu</span>
                  <span className="font-semibold">KES 0</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
