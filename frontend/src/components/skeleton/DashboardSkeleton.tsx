import { BaseSkeleton } from './BaseSkeleton'
import { CardSkeleton } from './CardSkeleton'
import { TableSkeleton } from './TableSkeleton'

export function DashboardSkeleton() {
  return (
    <div className="flex-1 p-8 space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <BaseSkeleton className="h-8 w-48 mb-2" />
          <BaseSkeleton className="h-4 w-64" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="rounded-xl border border-border bg-card p-6 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <BaseSkeleton className="h-4 w-24" />
              <BaseSkeleton className="h-8 w-8 rounded-full" />
            </div>
            <BaseSkeleton className="h-8 w-16" />
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <BaseSkeleton className="h-6 w-32" />
          <TableSkeleton rows={4} columns={5} />
        </div>
        <div className="space-y-4">
          <BaseSkeleton className="h-6 w-32" />
          <div className="space-y-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <CardSkeleton key={i} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
