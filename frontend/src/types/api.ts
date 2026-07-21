// ─── Generic API Response Wrappers ────────────────────────────────────────────

export interface ApiResponse<T = unknown> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T = unknown> {
  items: T[]
  pagination: {
    skip: number
    limit: number
    total: number
    cursor?: string | null
  }
}

// ─── API Error ────────────────────────────────────────────────────────────────

export interface ApiError {
  status: number
  detail: string
  code?: string
  errors?: Record<string, string[]>
}

// ─── Common Query Params ──────────────────────────────────────────────────────

export interface QueryParams {
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  search?: string
  status?: string
  created_after?: string
  created_before?: string
  cursor?: string
  limit?: number
}
