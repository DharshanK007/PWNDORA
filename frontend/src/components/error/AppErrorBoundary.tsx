import { Component, type ReactNode } from 'react'
import { AlertOctagon, RotateCcw } from 'lucide-react'
import { logger } from '@/services/logger'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class AppErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    logger.error('AppErrorBoundary', 'catch', 'Uncaught application error', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack
    })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen w-full flex-col items-center justify-center bg-background p-4 text-center text-foreground">
          <div className="mb-6 rounded-full bg-destructive/10 p-4">
            <AlertOctagon className="h-12 w-12 text-destructive" />
          </div>
          <h1 className="mb-2 text-2xl font-bold tracking-tight">Application Error</h1>
          <p className="mb-8 max-w-[500px] text-muted-foreground">
            A critical error occurred that prevented the application from rendering.
            {process.env.NODE_ENV === 'development' && (
              <span className="block mt-2 text-xs font-mono text-left bg-muted p-2 rounded text-destructive overflow-auto max-h-32">
                {this.state.error?.message}
              </span>
            )}
          </p>
          <div className="flex gap-4">
            <button
              onClick={() => window.location.reload()}
              className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            >
              <RotateCcw className="h-4 w-4" />
              Reload Application
            </button>
            <button
              onClick={() => {
                localStorage.clear()
                window.location.href = '/'
              }}
              className="inline-flex items-center gap-2 rounded-md border border-input bg-background px-4 py-2 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            >
              Clear Local Data & Restart
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
