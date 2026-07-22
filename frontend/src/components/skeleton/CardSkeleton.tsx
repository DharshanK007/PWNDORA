import { BaseSkeleton } from './BaseSkeleton'

export function CardSkeleton() {
  return (
    <div className="flex flex-col gap-3 p-4 border border-border rounded-xl bg-card">
      <div className="flex items-center gap-3">
        <BaseSkeleton className="h-10 w-10 rounded-full" />
        <div className="flex flex-col gap-2">
          <BaseSkeleton className="h-4 w-24" />
          <BaseSkeleton className="h-3 w-16" />
        </div>
      </div>
      <BaseSkeleton className="h-4 w-full mt-2" />
      <BaseSkeleton className="h-4 w-[80%]" />
      <div className="flex justify-between items-center mt-4">
        <BaseSkeleton className="h-8 w-20 rounded-md" />
        <BaseSkeleton className="h-8 w-20 rounded-md" />
      </div>
    </div>
  )
}
