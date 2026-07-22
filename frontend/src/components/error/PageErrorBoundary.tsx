import { Component, type ReactNode } from 'react'
import { AlertCircle, Home, RefreshCw } from 'lucide-react'
import { Link } from 'react-router-dom'
import { logger } from '@/services/logger'
import { ROUTES } from '@/constants/routes'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class PageErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    logger.error('PageErrorBoundary', 'catch', 'Page rendering error', {
      error: error.message,
      componentStack: errorInfo.componentStack
    })
  }

  resetError = () => {
    this.setState({ hasError: false, error: null })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-1 flex-col items-center justify-center p-8 text-center animate-fade-in">
          <div className="mb-6 rounded-full bg-destructive/10 p-6">
            <AlertCircle className="h-16 w-16 text-destructive" />
          </div>
          <h1 className="mb-2 text-3xl font-bold tracking-tight">Something went wrong</h1>
          <p className="mb-8 max-w-[500px] text-muted-foreground">
            We encountered an unexpected error while trying to load this page. 
            Our team has been notified. You can try refreshing the page or returning to the dashboard.
          </p>
          <div className="flex gap-4">
            <button
              onClick={this.resetError}
              className="inline-flex items-center gap-2 rounded-md bg-primary px-6 py-2.5 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            >
              <RefreshCw className="h-4 w-4" />
              Try Again
            </button>
            <Link
              to={ROUTES.DASHBOARD}
              onClick={this.resetError}
              className="inline-flex items-center gap-2 rounded-md border border-input bg-background px-6 py-2.5 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            >
              <Home className="h-4 w-4" />
              Go to Dashboard
            </Link>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
