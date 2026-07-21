import { cn } from '@/lib/utils'

export type StatusVariant = 'active' | 'inactive' | 'warning' | 'critical' | 'default'

interface StatusBadgeProps {
  status: string
  variant?: StatusVariant
  className?: string
}

export function StatusBadge({ status, variant = 'default', className }: StatusBadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wider',
        {
          'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20': variant === 'active',
          'bg-slate-500/15 text-slate-600 dark:text-slate-400 border border-slate-500/20': variant === 'inactive',
          'bg-amber-500/15 text-amber-600 dark:text-amber-400 border border-amber-500/20': variant === 'warning',
          'bg-red-500/15 text-red-600 dark:text-red-400 border border-red-500/20': variant === 'critical',
          'bg-blue-500/15 text-blue-600 dark:text-blue-400 border border-blue-500/20': variant === 'default',
        },
        className
      )}
    >
      {variant === 'active' && <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-emerald-500" />}
      {variant === 'warning' && <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-amber-500" />}
      {variant === 'critical' && <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-red-500 animate-pulse" />}
      {status}
    </span>
  )
}
