export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'user' | 'manager'
  createdAt: string
  updatedAt: string
  isActive: boolean
}

export interface Project {
  id: string
  name: string
  description?: string
  status: 'active' | 'completed' | 'archived'
  priority: 'low' | 'medium' | 'high'
  assigneeId?: string
  dueDate?: string
  createdAt: string
  updatedAt: string
}

export interface AuditLog {
  id: string
  userId: string
  action: string
  target: string
  targetId: string
  details: Record<string, any>
  timestamp: string
  ipAddress?: string
}