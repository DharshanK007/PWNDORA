import { cn } from '@/lib/utils'

interface CategoryBadgeProps {
  category: string
  className?: string
}

export function CategoryBadge({ category, className }: CategoryBadgeProps) {
  return (
    <span className={cn('px-2 py-0.5 rounded-md text-xs font-medium bg-primary/10 text-primary border border-primary/20', className)}>
      {category}
    </span>
  )
}
