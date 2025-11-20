import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { User } from '../types'
import { authApi } from '../services/api'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, username?: string) => Promise<void>
  logout: () => void
  updateUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: async (email: string, password: string) => {
        try {
          const response = await authApi.login({ email, password })
          // Assuming response contains user and token
          const user = response as any
          const token = 'mock-token' // Replace with actual token from response
          
          localStorage.setItem('auth_token', token)
          localStorage.setItem('user', JSON.stringify(user))
          
          set({
            user,
            token,
            isAuthenticated: true,
          })
        } catch (error) {
          throw error
        }
      },
      
      register: async (email: string, password: string, username?: string) => {
        try {
          const response = await authApi.register({ email, password, username })
          // Assuming response contains user and token
          const user = response as any
          const token = 'mock-token' // Replace with actual token from response
          
          localStorage.setItem('auth_token', token)
          localStorage.setItem('user', JSON.stringify(user))
          
          set({
            user,
            token,
            isAuthenticated: true,
          })
        } catch (error) {
          throw error
        }
      },
      
      logout: () => {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },
      
      updateUser: (user: User) => {
        localStorage.setItem('user', JSON.stringify(user))
        set({ user })
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

