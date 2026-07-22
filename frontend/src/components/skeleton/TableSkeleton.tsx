import { BaseSkeleton } from './BaseSkeleton'

interface TableSkeletonProps {
  rows?: number
  columns?: number
}

export function TableSkeleton({ rows = 5, columns = 4 }: TableSkeletonProps) {
  return (
    <div className="rounded-md border border-border bg-card overflow-hidden w-full">
      <div className="flex bg-muted/50 p-4 border-b border-border">
        {Array.from({ length: columns }).map((_, i) => (
          <div key={i} className="flex-1 pr-4">
            <BaseSkeleton className="h-4 w-20" />
          </div>
        ))}
      </div>
      <div className="divide-y divide-border">
        {Array.from({ length: rows }).map((_, i) => (
          <div key={i} className="flex p-4 items-center">
            {Array.from({ length: columns }).map((_, j) => (
              <div key={j} className="flex-1 pr-4">
                <BaseSkeleton className="h-4 w-[60%]" />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
