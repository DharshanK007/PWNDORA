import type { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface StatCardProps {
  title: string
  value: string | number
  icon: LucideIcon
  trend?: {
    value: string
    isPositive: boolean
  }
  variant?: 'default' | 'primary' | 'destructive' | 'warning'
}

export function StatCard({ title, value, icon: Icon, trend, variant = 'default' }: StatCardProps) {
  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-sm transition-all hover:shadow-md">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
        <div
          className={cn(
            'flex h-10 w-10 items-center justify-center rounded-lg',
            {
              'bg-primary/10 text-primary': variant === 'default' || variant === 'primary',
              'bg-destructive/10 text-destructive': variant === 'destructive',
              'bg-amber-500/10 text-amber-500': variant === 'warning',
            }
          )}
        >
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <div className="mt-4 flex items-baseline gap-2">
        <span className="text-3xl font-bold tracking-tight text-foreground">{value}</span>
        {trend && (
          <span
            className={cn(
              'text-xs font-medium',
              trend.isPositive ? 'text-emerald-500' : 'text-destructive'
            )}
          >
            {trend.isPositive ? '+' : '-'}{trend.value}
          </span>
        )}
      </div>
    </div>
  )
}
