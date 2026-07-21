// ─── String Helpers ───────────────────────────────────────────────────────────

export const truncate = (str: string, maxLength: number): string =>
  str.length > maxLength ? `${str.slice(0, maxLength)}…` : str

export const capitalize = (str: string): string =>
  str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()

export const getInitials = (name: string): string =>
  name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part.charAt(0).toUpperCase())
    .join('')

export const slugify = (str: string): string =>
  str
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^\w-]+/g, '')
    .replace(/--+/g, '-')
    .trim()

// ─── Array Helpers ────────────────────────────────────────────────────────────

export const groupBy = <T>(array: T[], keyFn: (item: T) => string): Record<string, T[]> =>
  array.reduce(
    (acc, item) => {
      const key = keyFn(item)
      acc[key] = [...(acc[key] ?? []), item]
      return acc
    },
    {} as Record<string, T[]>
  )

export const uniqueBy = <T>(array: T[], keyFn: (item: T) => string): T[] => {
  const seen = new Set<string>()
  return array.filter(item => {
    const key = keyFn(item)
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
}

// ─── Object Helpers ───────────────────────────────────────────────────────────

export const omitUndefined = <T extends Record<string, unknown>>(obj: T): Partial<T> =>
  Object.fromEntries(Object.entries(obj).filter(([, v]) => v !== undefined)) as Partial<T>

// ─── URL Helpers ──────────────────────────────────────────────────────────────

export const buildQueryString = (params: Record<string, unknown>): string => {
  const filtered = Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
  if (filtered.length === 0) return ''
  return '?' + new URLSearchParams(filtered.map(([k, v]) => [k, String(v)])).toString()
}
