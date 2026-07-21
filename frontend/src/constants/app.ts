// ─── Application Constants ────────────────────────────────────────────────────

export const APP = {
  NAME: 'NeoFactory Industries',
  SHORT_NAME: 'NeoFactory',
  VERSION: '1.0.0',
  DESCRIPTION: 'Enterprise Industrial IoT Operations Platform',
  COMPANY: 'NeoFactory Industries',
} as const

// ─── Pagination ────────────────────────────────────────────────────────────────

export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 25,
  PAGE_SIZE_OPTIONS: [10, 25, 50, 100],
} as const

// ─── Storage Keys ─────────────────────────────────────────────────────────────

export const STORAGE_KEYS = {
  AUTH_TOKEN: 'nf_access_token',
  THEME: 'nf_theme',
  SIDEBAR_COLLAPSED: 'nf_sidebar_collapsed',
} as const

// ─── Theme ────────────────────────────────────────────────────────────────────

export type Theme = 'light' | 'dark' | 'system'

export const THEMES: Theme[] = ['light', 'dark', 'system']

// ─── Status Labels ────────────────────────────────────────────────────────────

export const STATUS_LABELS: Record<string, string> = {
  ACTIVE: 'Active',
  INACTIVE: 'Inactive',
  PENDING: 'Pending',
  APPROVED: 'Approved',
  REJECTED: 'Rejected',
  ASSIGNED: 'Assigned',
  IN_PROGRESS: 'In Progress',
  COMPLETED: 'Completed',
  FAILED: 'Failed',
  CANCELLED: 'Cancelled',
} as const
