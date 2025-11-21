import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { User } from '../types'
import { authApi } from '../services/api'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, username: string) => Promise<void>
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
          // LoginResponse contains user_id, token, and email
          const user = {
            user_id: response.user_id,
            email: response.email,
            is_active: true,
            is_verified: false,
            created_at: Date.now(), // We don't have this from login, use current time
          }
          const token = response.token
          
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
      
      register: async (email: string, password: string, username: string) => {
        try {
          // Register the user
          const registerResponse = await authApi.register({ 
            email, 
            password, 
            username
          })
          
          // After successful registration, automatically log in
          const loginResponse = await authApi.login({ email, password })
          
          // LoginResponse contains user_id, token, and email
          const user = {
            user_id: loginResponse.user_id,
            email: loginResponse.email,
            username: username,
            is_active: true,
            is_verified: false,
            created_at: registerResponse.created_at,
          }
          const token = loginResponse.token
          
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
      onRehydrateStorage: () => (state) => {
        // Recalculate isAuthenticated after rehydration from localStorage
        if (state) {
          // Also check the actual localStorage values to ensure consistency
          const token = localStorage.getItem('auth_token')
          const userStr = localStorage.getItem('user')
          const hasValidAuth = !!(token && userStr && state.user && state.token)
          state.isAuthenticated = hasValidAuth
          if (!hasValidAuth) {
            // Clear invalid state
            state.user = null
            state.token = null
            state.isAuthenticated = false
            localStorage.removeItem('auth_token')
            localStorage.removeItem('user')
          }
        }
      },
    }
  )
)

