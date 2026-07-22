import { cn } from '@/lib/utils'

interface BaseSkeletonProps extends React.HTMLAttributes<HTMLDivElement> {}

export function BaseSkeleton({ className, ...props }: BaseSkeletonProps) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-muted/60', className)}
      {...props}
    />
  )
}
