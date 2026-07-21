import { ChevronRight, Home } from 'lucide-react'
import { Link } from 'react-router-dom'
import type { Breadcrumb } from '@/types/common'
import { ROUTES } from '@/constants/routes'
import { cn } from '@/lib/utils'

// ─── Breadcrumbs ──────────────────────────────────────────────────────────────

interface BreadcrumbsProps {
  items: Breadcrumb[]
  className?: string
}

export function Breadcrumbs({ items, className }: BreadcrumbsProps) {
  return (
    <nav aria-label="Breadcrumb" className={cn('flex items-center gap-1', className)}>
      <Link
        to={ROUTES.DASHBOARD}
        className="text-muted-foreground hover:text-foreground transition-colors"
        aria-label="Home"
      >
        <Home className="h-3.5 w-3.5" />
      </Link>

      {items.map((item, index) => (
        <div key={index} className="flex items-center gap-1">
          <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/50 flex-shrink-0" />
          {item.href && index < items.length - 1 ? (
            <Link
              to={item.href}
              className="text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              {item.label}
            </Link>
          ) : (
            <span
              className={cn(
                'text-xs',
                index === items.length - 1
                  ? 'font-medium text-foreground'
                  : 'text-muted-foreground'
              )}
              aria-current={index === items.length - 1 ? 'page' : undefined}
            >
              {item.label}
            </span>
          )}
        </div>
      ))}
    </nav>
  )
}
