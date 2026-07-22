import { Target, Play } from 'lucide-react'
import { Link } from 'react-router-dom'
import { ROUTES } from '@/constants/routes'

interface EmptyScenarioProps {
  title?: string
  description?: string
  actionLabel?: string
  onAction?: () => void
}

export function EmptyScenario({
  title = 'No Scenarios Available',
  description = 'There are no active scenarios for you to investigate right now. Check back later or adjust your filters.',
  actionLabel = 'View Catalog',
  onAction
}: EmptyScenarioProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center animate-in fade-in duration-300">
      <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-primary/10 border border-primary/20 shadow-sm">
        <Target className="h-10 w-10 text-primary" />
      </div>
      <h3 className="mb-2 text-xl font-bold tracking-tight text-foreground">{title}</h3>
      <p className="mb-8 max-w-md text-sm text-muted-foreground leading-relaxed">
        {description}
      </p>
      
      {onAction ? (
        <button
          onClick={onAction}
          className="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-primary px-6 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          <Play className="h-4 w-4 fill-current" />
          {actionLabel}
        </button>
      ) : (
        <Link
          to={ROUTES.SCENARIOS}
          className="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-primary px-6 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          <Play className="h-4 w-4 fill-current" />
          {actionLabel}
        </Link>
      )}
    </div>
  )
}
