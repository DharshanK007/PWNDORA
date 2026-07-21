import { ChevronRight, Home } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useBreadcrumbs } from '@/hooks/useBreadcrumbs'
import { cn } from '@/lib/utils'

export function BreadcrumbBar() {
  const breadcrumbs = useBreadcrumbs()

  if (breadcrumbs.length === 0) return null

  return (
    <nav aria-label="Breadcrumb" className="hidden md:flex items-center px-4 py-2 bg-card/50 border-b border-border text-sm">
      <ol className="flex items-center space-x-2">
        {breadcrumbs.map((bc, index) => {
          const isLast = index === breadcrumbs.length - 1
          
          return (
            <li key={`${bc.label}-${index}`} className="flex items-center">
              {index > 0 && <ChevronRight className="h-4 w-4 mx-2 text-muted-foreground shrink-0" />}
              {bc.href ? (
                <Link
                  to={bc.href}
                  className={cn(
                    'transition-colors font-medium flex items-center gap-1.5',
                    isLast 
                      ? 'text-foreground pointer-events-none' 
                      : 'text-muted-foreground hover:text-foreground'
                  )}
                  aria-current={isLast ? 'page' : undefined}
                >
                  {index === 0 && <Home className="h-3.5 w-3.5" />}
                  {bc.label}
                </Link>
              ) : (
                <span className="text-muted-foreground font-medium">{bc.label}</span>
              )}
            </li>
          )
        })}
      </ol>
    </nav>
  )
}
