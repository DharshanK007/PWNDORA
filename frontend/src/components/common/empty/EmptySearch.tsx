import { Search } from 'lucide-react'

interface EmptySearchProps {
  title?: string
  description?: string
  onClear?: () => void
}

export function EmptySearch({
  title = 'No results found',
  description = "We couldn't find anything matching your search criteria. Try adjusting your filters or search terms.",
  onClear
}: EmptySearchProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center animate-in fade-in duration-300">
      <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-muted/50">
        <Search className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="mb-2 text-lg font-semibold text-foreground">{title}</h3>
      <p className="mb-6 max-w-sm text-sm text-muted-foreground">
        {description}
      </p>
      {onClear && (
        <button
          onClick={onClear}
          className="text-sm font-medium text-primary hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded"
        >
          Clear search & filters
        </button>
      )}
    </div>
  )
}
