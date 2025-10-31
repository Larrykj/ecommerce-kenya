import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface LanguageStore {
  language: 'en' | 'sw'
  setLanguage: (lang: 'en' | 'sw') => void
  toggleLanguage: () => void
}

export const useLanguageStore = create<LanguageStore>()(
  persist(
    (set, get) => ({
      language: 'en',
      setLanguage: (lang) => set({ language: lang }),
      toggleLanguage: () => set({ language: get().language === 'en' ? 'sw' : 'en' })
    }),
    {
      name: 'language-storage'
    }
  )
)

