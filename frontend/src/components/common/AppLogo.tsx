import { Factory } from 'lucide-react'
import { cn } from '@/lib/utils'
import { APP } from '@/constants/app'

// ─── App Logo ─────────────────────────────────────────────────────────────────

interface AppLogoProps {
  collapsed?: boolean
  className?: string
}

export function AppLogo({ collapsed = false, className }: AppLogoProps) {
  return (
    <div className={cn('flex items-center gap-2.5', className)}>
      <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-primary">
        <Factory className="h-4.5 w-4.5 text-primary-foreground" strokeWidth={2} />
      </div>
      {!collapsed && (
        <div className="flex flex-col leading-none">
          <span className="text-sm font-bold tracking-tight text-foreground">
            {APP.SHORT_NAME}
          </span>
          <span className="text-[10px] font-medium uppercase tracking-widest text-muted-foreground">
            Industries
          </span>
        </div>
      )}
    </div>
  )
}
