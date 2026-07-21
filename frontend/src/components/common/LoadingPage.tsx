import { LoadingSpinner } from './LoadingSpinner'
import { APP } from '@/constants/app'

// ─── Full Page Loading ────────────────────────────────────────────────────────

interface LoadingPageProps {
  message?: string
}

export function LoadingPage({ message = 'Loading…' }: LoadingPageProps) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background">
      <LoadingSpinner size="lg" />
      <div className="text-center">
        <p className="text-sm font-medium text-foreground">{message}</p>
        <p className="text-xs text-muted-foreground">{APP.NAME}</p>
      </div>
    </div>
  )
}
