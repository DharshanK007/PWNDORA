import { cn } from '@/lib/utils'

interface ScenarioProgressProps {
  status: 'Not Started' | 'In Progress' | 'Completed'
  percentage?: number
  className?: string
}

export function ScenarioProgress({ status, percentage = 0, className }: ScenarioProgressProps) {
  let statusColor = 'bg-slate-500'
  let textColor = 'text-slate-500 dark:text-slate-400'

  if (status === 'Completed') {
    statusColor = 'bg-emerald-500'
    textColor = 'text-emerald-600 dark:text-emerald-400'
    percentage = 100
  } else if (status === 'In Progress') {
    statusColor = 'bg-blue-500'
    textColor = 'text-blue-600 dark:text-blue-400'
  } else {
    percentage = 0
  }

  return (
    <div className={cn('space-y-1.5', className)}>
      <div className="flex items-center justify-between text-xs font-medium">
        <span className={textColor}>{status}</span>
        {status !== 'Not Started' && <span className="text-muted-foreground">{percentage}%</span>}
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
        <div 
          className={cn('h-full rounded-full transition-all duration-500', statusColor)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}
