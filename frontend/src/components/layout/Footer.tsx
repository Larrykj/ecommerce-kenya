'use client'

import Link from 'next/link'
import { FiFacebook, FiTwitter, FiInstagram, FiMail, FiPhone } from 'react-icons/fi'
import { useLanguageStore } from '@/store/languageStore'

export default function Footer() {
  const { language } = useLanguageStore()
  const isSwahili = language === 'sw'

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* About */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">
              {isSwahili ? 'Kuhusu ShopKE' : 'About ShopKE'}
            </h3>
            <p className="text-sm">
              {isSwahili 
                ? 'Jukwaa la biashara la Kenya linalotumia AI kutoa mapendekezo ya kibinafsi kwa watumiaji wote.'
                : 'Kenya\'s AI-powered e-commerce platform providing personalized recommendations for every shopper.'}
            </p>
            <div className="flex space-x-4 mt-4">
              <a href="#" className="hover:text-primary-400"><FiFacebook size={20} /></a>
              <a href="#" className="hover:text-primary-400"><FiTwitter size={20} /></a>
              <a href="#" className="hover:text-primary-400"><FiInstagram size={20} /></a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">
              {isSwahili ? 'Viungo vya Haraka' : 'Quick Links'}
            </h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/about" className="hover:text-primary-400">{isSwahili ? 'Kuhusu Sisi' : 'About Us'}</Link></li>
              <li><Link href="/how-it-works" className="hover:text-primary-400">{isSwahili ? 'Jinsi Inavyofanya Kazi' : 'How It Works'}</Link></li>
              <li><Link href="/vendors" className="hover:text-primary-400">{isSwahili ? 'Kuwa Muuzaji' : 'Become a Vendor'}</Link></li>
              <li><Link href="/help" className="hover:text-primary-400">{isSwahili ? 'Msaada' : 'Help Center'}</Link></li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">
              {isSwahili ? 'Huduma kwa Wateja' : 'Customer Service'}
            </h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/shipping" className="hover:text-primary-400">{isSwahili ? 'Usafirishaji' : 'Shipping Info'}</Link></li>
              <li><Link href="/returns" className="hover:text-primary-400">{isSwahili ? 'Rejesha Bidhaa' : 'Returns & Refunds'}</Link></li>
              <li><Link href="/mpesa" className="hover:text-primary-400">{isSwahili ? 'Malipo ya M-Pesa' : 'M-Pesa Payments'}</Link></li>
              <li><Link href="/faq" className="hover:text-primary-400">{isSwahili ? 'Maswali ya Kawaida' : 'FAQ'}</Link></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">
              {isSwahili ? 'Wasiliana Nasi' : 'Contact Us'}
            </h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center space-x-2">
                <FiMail size={16} />
                <a href="mailto:support@shopke.co.ke" className="hover:text-primary-400">support@shopke.co.ke</a>
              </li>
              <li className="flex items-center space-x-2">
                <FiPhone size={16} />
                <a href="tel:+254712345678" className="hover:text-primary-400">+254 712 345 678</a>
              </li>
            </ul>
            
            {/* Payment Methods */}
            <div className="mt-6">
              <p className="text-sm font-semibold mb-2">{isSwahili ? 'Njia za Malipo' : 'Payment Methods'}</p>
              <div className="flex items-center space-x-2">
                <div className="bg-white px-3 py-1 rounded text-green-600 font-bold text-sm">M-PESA</div>
                <div className="bg-white px-3 py-1 rounded text-blue-600 font-bold text-xs">VISA</div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center text-sm">
          <p>&copy; 2024 ShopKE. {isSwahili ? 'Haki zote zimehifadhiwa.' : 'All rights reserved.'}</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link href="/privacy" className="hover:text-primary-400">{isSwahili ? 'Sera ya Faragha' : 'Privacy Policy'}</Link>
            <Link href="/terms" className="hover:text-primary-400">{isSwahili ? 'Masharti' : 'Terms of Service'}</Link>
            <Link href="/cookies" className="hover:text-primary-400">{isSwahili ? 'Sera ya Kuki' : 'Cookie Policy'}</Link>
          </div>
        </div>

        {/* Made in Kenya Badge */}
        <div className="text-center mt-6">
          <p className="text-xs text-gray-500">
            🇰🇪 {isSwahili ? 'Iliyotengenezwa kwa Kenya, na Wakenyans' : 'Made in Kenya, for Kenyans'}
          </p>
        </div>
      </div>
    </footer>
  )
}

