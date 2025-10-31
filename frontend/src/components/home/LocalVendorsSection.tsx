'use client'

import Link from 'next/link'
import { useLanguageStore } from '@/store/languageStore'

interface LocalVendorsSectionProps {
  county?: string | null
  title: string
  titleEn: string
}

export default function LocalVendorsSection({ county, title, titleEn }: LocalVendorsSectionProps) {
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'

  // Mock vendors
  const vendors = []

  return (
    <section className="bg-gradient-to-r from-kenyan-green/10 to-kenyan-red/10 rounded-2xl p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900">
            {isSwahili ? title : titleEn}
          </h2>
          <p className="text-gray-600 mt-1 flex items-center">
            🇰🇪 {isSwahili 
              ? 'Unga mkono biashara za Wakenya' 
              : 'Support Kenyan businesses'}
          </p>
        </div>
        <Link 
          href="/local-vendors" 
          className="text-primary-600 font-semibold hover:text-primary-700"
        >
          {isSwahili ? 'Tazama Wote →' : 'View All →'}
        </Link>
      </div>

      {vendors.length === 0 ? (
        <div className="bg-white rounded-lg p-12 text-center">
          <div className="text-5xl mb-4">🏪</div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {isSwahili 
              ? 'Wafanyabiashara wa Ndani Wanakuja!' 
              : 'Local Vendors Coming Soon!'}
          </h3>
          <p className="text-gray-600 mb-4">
            {isSwahili
              ? `Tunajenga mtandao wa wafanyabiashara kutoka ${county || 'Kenya'}`
              : `We're building a network of vendors from ${county || 'Kenya'}`}
          </p>
          <Link 
            href="/become-vendor" 
            className="inline-block bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
          >
            {isSwahili ? 'Jiunge Sasa' : 'Become a Vendor'}
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {/* Vendor cards will go here */}
        </div>
      )}
    </section>
  )
}

