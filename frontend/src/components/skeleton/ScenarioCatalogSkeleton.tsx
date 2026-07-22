import { BaseSkeleton } from './BaseSkeleton'
import { CardSkeleton } from './CardSkeleton'

export function ScenarioCatalogSkeleton() {
  return (
    <div className="flex-1 p-4 md:p-8 space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <BaseSkeleton className="h-8 w-48 mb-2" />
          <BaseSkeleton className="h-4 w-64" />
        </div>
        <div className="flex items-center gap-3 w-full md:w-auto">
          <BaseSkeleton className="h-10 w-64 rounded-md" />
          <BaseSkeleton className="h-10 w-24 rounded-md" />
        </div>
      </div>

      <div className="flex gap-2">
        {Array.from({ length: 4 }).map((_, i) => (
          <BaseSkeleton key={i} className="h-8 w-24 rounded-full" />
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {Array.from({ length: 8 }).map((_, i) => (
          <CardSkeleton key={i} />
        ))}
      </div>
    </div>
  )
}
