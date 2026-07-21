import { FileQuestion, ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '@/constants/routes'

// ─── Not Found (404) ──────────────────────────────────────────────────────────

export function NotFound() {
  const navigate = useNavigate()

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 bg-background p-6 text-center">
      <div className="space-y-2">
        <p className="text-8xl font-extrabold tracking-tight text-primary/20">404</p>
      </div>
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted">
        <FileQuestion className="h-8 w-8 text-muted-foreground" />
      </div>
      <div className="space-y-2">
        <h1 className="text-2xl font-bold text-foreground">Page not found</h1>
        <p className="max-w-md text-sm text-muted-foreground">
          The page you are looking for does not exist or has been moved. Please
          check the URL or navigate back to the dashboard.
        </p>
      </div>
      <div className="flex gap-3">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-2 rounded-lg border border-border bg-background px-4 py-2 text-sm font-medium text-foreground hover:bg-muted transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Go Back
        </button>
        <button
          onClick={() => navigate(ROUTES.DASHBOARD)}
          className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
        >
          Go to Dashboard
        </button>
      </div>
    </div>
  )
}
