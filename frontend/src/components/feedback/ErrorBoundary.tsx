import { Component, type ReactNode, type ErrorInfo } from 'react'
import { AlertTriangle, RefreshCw, LayoutDashboard } from 'lucide-react'
import { ROUTES } from '@/constants/routes'
import { APP } from '@/constants/app'

// ─── Error Boundary State ─────────────────────────────────────────────────────

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

// ─── Error Boundary Props ─────────────────────────────────────────────────────

interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
}

// ─── Error Boundary ───────────────────────────────────────────────────────────

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error('[ErrorBoundary]', error, info.componentStack)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null })
  }

  handleGoHome = () => {
    window.location.href = ROUTES.DASHBOARD
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback

      return (
        <div className="flex min-h-screen items-center justify-center bg-background p-6">
          <div className="flex max-w-md flex-col items-center gap-6 rounded-2xl border border-border bg-card p-10 shadow-lg text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10">
              <AlertTriangle className="h-8 w-8 text-destructive" />
            </div>
            <div className="space-y-2">
              <h1 className="text-xl font-semibold text-foreground">
                Something went wrong
              </h1>
              <p className="text-sm text-muted-foreground">
                {APP.NAME} encountered an unexpected error. Your session and data are safe.
              </p>
              {this.state.error && (
                <p className="mt-2 rounded-md bg-muted px-3 py-2 text-xs text-muted-foreground font-mono">
                  {this.state.error.message}
                </p>
              )}
            </div>
            <div className="flex gap-3">
              <button
                onClick={this.handleRetry}
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                <RefreshCw className="h-4 w-4" />
                Retry
              </button>
              <button
                onClick={this.handleGoHome}
                className="inline-flex items-center gap-2 rounded-lg border border-border bg-background px-4 py-2 text-sm font-medium text-foreground hover:bg-muted transition-colors"
              >
                <LayoutDashboard className="h-4 w-4" />
                Dashboard
              </button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
