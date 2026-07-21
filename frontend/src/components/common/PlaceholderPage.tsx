import type { LucideIcon } from 'lucide-react'
import { Hammer } from 'lucide-react'

interface PlaceholderPageProps {
  title: string
  description?: string
  icon?: LucideIcon
}

export function PlaceholderPage({
  title,
  description = 'This enterprise module is currently under development.',
  icon: Icon = Hammer,
}: PlaceholderPageProps) {
  return (
    <div className="flex h-full flex-col items-center justify-center text-center animate-fade-in p-8">
      <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-primary/10 mb-6">
        <Icon className="h-10 w-10 text-primary" />
      </div>
      <h2 className="text-2xl font-bold tracking-tight text-foreground mb-2">
        {title}
      </h2>
      <p className="text-muted-foreground max-w-md mb-8">
        {description}
      </p>
      <div className="inline-flex items-center rounded-full border border-border bg-background px-4 py-1.5 text-sm font-medium shadow-sm">
        <span className="flex h-2 w-2 rounded-full bg-amber-500 mr-2 animate-pulse"></span>
        Coming Soon
      </div>
    </div>
  )
}
