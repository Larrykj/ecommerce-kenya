/** @type {import('next').NextConfig} */
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development'
})

const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost', 'your-cdn-domain.com'],
    formats: ['image/avif', 'image/webp']
  },
  i18n: {
    locales: ['en', 'sw'],
    defaultLocale: 'en'
  },
  env: {
    API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  },
  // Optimize for low-bandwidth
  compress: true,
  poweredByHeader: false,
  // Enable SWC minification
  swcMinify: true
}

module.exports = withPWA(nextConfig)

