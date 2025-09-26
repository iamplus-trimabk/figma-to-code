import { useState, useCallback } from 'react'

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  headers?: Record<string, string>
  body?: any
}

interface UseApiReturn {
  data: any
  loading: boolean
  error: string | null
  execute: (options?: ApiOptions) => Promise<void>
}

export function useApi(url: string, options: ApiOptions = {}): UseApiReturn {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  const execute = useCallback(async (executeOptions: ApiOptions = {}) => {
    setLoading(true)
    setError(null)

    try {
      const finalOptions = {
        ...options,
        ...executeOptions,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
          ...executeOptions.headers,
        },
      }

      // Add auth token if available
      const token = localStorage.getItem('auth-token')
      if (token) {
        finalOptions.headers = {
          ...finalOptions.headers,
          Authorization: `Bearer ${token}`,
        }
      }

      const response = await fetch(url, {
        method: finalOptions.method || 'GET',
        headers: finalOptions.headers,
        body: finalOptions.body ? JSON.stringify(finalOptions.body) : undefined,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }, [url, options])

  // Auto-execute on mount if it's a GET request
  useState(() => {
    if (!options.method || options.method === 'GET') {
      execute()
    }
  })

  return {
    data,
    loading,
    error,
    execute,
  }
}