import type { LucideIcon } from 'lucide-react'
import { FileX2 } from 'lucide-react'

interface EmptyModuleProps {
  title: string
  description?: string
  icon?: LucideIcon
  action?: React.ReactNode
}

export function EmptyModule({ 
  title, 
  description = 'No data available at this time.',
  icon: Icon = FileX2,
  action
}: EmptyModuleProps) {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center rounded-xl border border-dashed border-border bg-card/50 p-8 text-center animate-fade-in">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted mb-4">
        <Icon className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold text-foreground">{title}</h3>
      <p className="mt-2 max-w-sm text-sm text-muted-foreground">{description}</p>
      {action && <div className="mt-6">{action}</div>}
    </div>
  )
}
