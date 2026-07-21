// ─── Date & Time Formatters ───────────────────────────────────────────────────

export const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '—'
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(new Date(dateString))
}

export const formatDateTime = (dateString: string | null | undefined): string => {
  if (!dateString) return '—'
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(dateString))
}

export const formatRelativeTime = (dateString: string | null | undefined): string => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60_000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h ago`
  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 30) return `${diffDays}d ago`
  return formatDate(dateString)
}

// ─── Number Formatters ────────────────────────────────────────────────────────

export const formatNumber = (value: number): string =>
  new Intl.NumberFormat('en-US').format(value)

export const formatCurrency = (value: number, currency = 'USD'): string =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value)

export const formatPercent = (value: number, decimals = 1): string =>
  `${value.toFixed(decimals)}%`

export const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`
}

// ─── Status Label Formatter ───────────────────────────────────────────────────

export const formatStatus = (status: string): string =>
  status
    .toLowerCase()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
