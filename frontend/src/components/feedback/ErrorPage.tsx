import { AlertTriangle, RefreshCw, Home } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '@/constants/routes'

// ─── Error Page ───────────────────────────────────────────────────────────────

interface ErrorPageProps {
  title?: string
  message?: string
  onRetry?: () => void
}

export function ErrorPage({
  title = 'Unable to load content',
  message = 'An error occurred while loading this page. Please try again.',
  onRetry,
}: ErrorPageProps) {
  const navigate = useNavigate()

  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center gap-6 rounded-xl border border-border bg-card p-10 text-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-full bg-destructive/10">
        <AlertTriangle className="h-7 w-7 text-destructive" />
      </div>
      <div className="space-y-1.5">
        <h2 className="text-lg font-semibold text-foreground">{title}</h2>
        <p className="max-w-sm text-sm text-muted-foreground">{message}</p>
      </div>
      <div className="flex gap-3">
        {onRetry && (
          <button
            onClick={onRetry}
            className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            <RefreshCw className="h-4 w-4" />
            Try Again
          </button>
        )}
        <button
          onClick={() => navigate(ROUTES.DASHBOARD)}
          className="inline-flex items-center gap-2 rounded-lg border border-border bg-background px-4 py-2 text-sm font-medium text-foreground hover:bg-muted transition-colors"
        >
          <Home className="h-4 w-4" />
          Dashboard
        </button>
      </div>
    </div>
  )
}
