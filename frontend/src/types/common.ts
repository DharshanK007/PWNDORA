// ─── UI Primitives ────────────────────────────────────────────────────────────

export interface SelectOption<T = string> {
  label: string
  value: T
  disabled?: boolean
}

export type SortOrder = 'asc' | 'desc'

export interface Breadcrumb {
  label: string
  href?: string
}

// ─── Status Types ─────────────────────────────────────────────────────────────

export type StatusVariant = 'default' | 'success' | 'warning' | 'error' | 'info' | 'pending'

export interface StatusConfig {
  label: string
  variant: StatusVariant
}

// ─── Filter Params ────────────────────────────────────────────────────────────

export interface FilterParams {
  search?: string
  status?: string
  department?: string
  location?: string
  created_after?: string
  created_before?: string
}

// ─── Table Column ─────────────────────────────────────────────────────────────

export interface TableColumn<T = Record<string, unknown>> {
  key: keyof T | string
  label: string
  sortable?: boolean
  className?: string
  render?: (value: unknown, row: T) => React.ReactNode
}

// ─── Notification ─────────────────────────────────────────────────────────────

export type NotificationPriority = 'INFO' | 'SUCCESS' | 'WARNING' | 'ERROR' | 'CRITICAL'

export interface NotificationItem {
  id: string
  title: string
  message: string
  priority: NotificationPriority
  read: boolean
  created_at: string
}
