import type { ReactNode } from 'react'

interface InfoPanelProps {
  title: string
  description?: string
  children: ReactNode
  actions?: ReactNode
}

export function InfoPanel({ title, description, children, actions }: InfoPanelProps) {
  return (
    <div className="rounded-xl border border-border bg-card shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border p-5">
        <div>
          <h2 className="text-lg font-semibold text-foreground">{title}</h2>
          {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
        </div>
        {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
      </div>
      <div className="p-5">{children}</div>
    </div>
  )
}
