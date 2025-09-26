import React from 'react'
import { cn } from '@/shadcn/lib/utils'

export interface CustomComponentProps {
  className?: string
  children?: React.ReactNode
}

export function CustomComponent({ className, children }: CustomComponentProps) {
  return (
    <div className={cn('p-4 border rounded-lg bg-card', className)}>
      {children}
    </div>
  )
}
