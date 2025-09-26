import { useState, useEffect } from 'react'

export function useCustomHook(initialValue: any) {
  const [value, setValue] = useState(initialValue)

  useEffect(() => {
    // Add your side effect logic here
  }, [value])

  return [value, setValue]
}
