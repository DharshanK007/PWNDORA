import { FolderOpen } from 'lucide-react'

interface EmptyTableProps {
  title?: string
  description?: string
  actionLabel?: string
  onAction?: () => void
}

export function EmptyTable({
  title = 'No data available',
  description = 'There are no records to display in this table yet.',
  actionLabel,
  onAction
}: EmptyTableProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center animate-in fade-in duration-300">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-muted/50 border border-border">
        <FolderOpen className="h-6 w-6 text-muted-foreground" />
      </div>
      <h3 className="mb-1 text-sm font-semibold text-foreground">{title}</h3>
      <p className="mb-6 text-sm text-muted-foreground max-w-sm">
        {description}
      </p>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="inline-flex h-9 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          {actionLabel}
        </button>
      )}
    </div>
  )
}
