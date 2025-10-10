/**
 * Hook to load layout data asynchronously
 */
'use client'
import { useState, useEffect } from 'react'

export function useLayoutData() {
  const [layoutData, setLayoutData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        const response = await fetch('/extracted_login_assets_api/screen_layouts.json')
        if (!response.ok) {
          throw new Error(`Failed to load: ${response.status}`)
        }
        const data = await response.json()
        setLayoutData(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setLayoutData(null)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  return { layoutData, loading, error }
}