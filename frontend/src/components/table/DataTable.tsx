import { useState } from 'react'
import { ChevronDown, ChevronUp, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface Column<T> {
  key: string
  header: string
  cell?: (item: T) => React.ReactNode
  sortable?: boolean
  className?: string
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
  isLoading?: boolean
  emptyMessage?: string
  keyExtractor: (item: T) => string | number
  onSort?: (key: string, direction: 'asc' | 'desc') => void
}

export function DataTable<T>({
  data,
  columns,
  isLoading,
  emptyMessage = 'No data available',
  keyExtractor,
  onSort
}: DataTableProps<T>) {
  const [sortKey, setSortKey] = useState<string | null>(null)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc')

  const handleSort = (key: string) => {
    let newDirection: 'asc' | 'desc' = 'asc'
    if (sortKey === key) {
      newDirection = sortDirection === 'asc' ? 'desc' : 'asc'
    }
    setSortKey(key)
    setSortDirection(newDirection)
    if (onSort) onSort(key, newDirection)
  }

  return (
    <div className="w-full overflow-x-auto rounded-xl border border-border bg-card shadow-sm">
      <table className="w-full text-left text-sm text-foreground">
        <thead className="border-b border-border bg-muted/50 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className={cn('px-4 py-3', col.className, col.sortable && 'cursor-pointer hover:text-foreground')}
                onClick={() => col.sortable && handleSort(col.key)}
              >
                <div className="flex items-center gap-1">
                  {col.header}
                  {col.sortable && sortKey === col.key && (
                    sortDirection === 'asc' ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {isLoading ? (
            <tr>
              <td colSpan={columns.length} className="px-4 py-8 text-center">
                <div className="flex flex-col items-center justify-center text-muted-foreground">
                  <Loader2 className="h-6 w-6 animate-spin mb-2" />
                  <p>Loading data...</p>
                </div>
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="px-4 py-8 text-center text-muted-foreground">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((item) => (
              <tr key={keyExtractor(item)} className="transition-colors hover:bg-muted/30">
                {columns.map((col) => (
                  <td key={col.key} className={cn('px-4 py-3 whitespace-nowrap', col.className)}>
                    {col.cell ? col.cell(item) : String((item as Record<string, unknown>)[col.key] ?? '')}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
      {/* Pagination footer placeholder - can be expanded later */}
      {!isLoading && data.length > 0 && (
        <div className="border-t border-border bg-muted/10 px-4 py-3 text-xs text-muted-foreground flex items-center justify-between">
          <span>Showing {data.length} entries</span>
        </div>
      )}
    </div>
  )
}
