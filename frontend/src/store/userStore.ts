import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  name: string
  email: string
  county?: string
  preferredLanguage: string
}

interface UserStore {
  user: User | null
  county: string | null
  setUser: (user: User | null) => void
  setCounty: (county: string) => void
  logout: () => void
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      user: null,
      county: null,
      setUser: (user) => set({ user }),
      setCounty: (county) => set({ county }),
      logout: () => set({ user: null, county: null })
    }),
    {
      name: 'user-storage',
    }
  )
)

