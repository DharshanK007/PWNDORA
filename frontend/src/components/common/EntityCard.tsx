import type { ReactNode } from 'react'

interface EntityCardProps {
  title: string
  subtitle?: string
  icon?: ReactNode
  badges?: ReactNode
  children?: ReactNode
  footer?: ReactNode
}

export function EntityCard({ title, subtitle, icon, badges, children, footer }: EntityCardProps) {
  return (
    <div className="flex flex-col rounded-xl border border-border bg-card shadow-sm transition-all hover:shadow-md hover:border-primary/20">
      <div className="flex items-start justify-between p-5 pb-4">
        <div className="flex items-start gap-4">
          {icon && (
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
              {icon}
            </div>
          )}
          <div>
            <h3 className="font-semibold leading-none text-foreground">{title}</h3>
            {subtitle && <p className="mt-1.5 text-sm text-muted-foreground">{subtitle}</p>}
          </div>
        </div>
        {badges && <div className="flex gap-2">{badges}</div>}
      </div>
      
      {children && (
        <div className="px-5 py-4 flex-1 border-t border-border/50 bg-muted/10">
          {children}
        </div>
      )}
      
      {footer && (
        <div className="px-5 py-3 border-t border-border bg-muted/30 mt-auto rounded-b-xl text-sm">
          {footer}
        </div>
      )}
    </div>
  )
}
