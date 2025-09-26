import { useState, useEffect } from 'react'

interface User {
  id: string
  email: string
  name: string
  role: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  })

  useEffect(() => {
    // Check for existing auth token and validate it
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('auth-token')
        if (token) {
          // Validate token with API
          const response = await fetch('/api/auth/validate', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })

          if (response.ok) {
            const user = await response.json()
            setAuthState({
              user,
              isAuthenticated: true,
              isLoading: false,
            })
          } else {
            // Token is invalid
            localStorage.removeItem('auth-token')
            setAuthState({
              user: null,
              isAuthenticated: false,
              isLoading: false,
            })
          }
        } else {
          setAuthState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          })
        }
      } catch (error) {
        console.error('Auth check failed:', error)
        setAuthState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
        })
      }
    }

    checkAuth()
  }, [])

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (response.ok) {
        const { user, token } = await response.json()
        localStorage.setItem('auth-token', token)
        setAuthState({
          user,
          isAuthenticated: true,
          isLoading: false,
        })
        return { success: true }
      } else {
        return { success: false, error: 'Invalid credentials' }
      }
    } catch (error) {
      return { success: false, error: 'Network error' }
    }
  }

  const logout = () => {
    localStorage.removeItem('auth-token')
    setAuthState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    })
  }

  return {
    ...authState,
    login,
    logout,
  }
}