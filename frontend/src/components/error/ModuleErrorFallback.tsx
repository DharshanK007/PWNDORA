import { Component, type ReactNode } from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'
import { logger } from '@/services/logger'

interface Props {
  children: ReactNode
  moduleName: string
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ModuleErrorFallback extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    logger.error('ModuleErrorFallback', 'catch', `Module error in ${this.props.moduleName}`, {
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
        <div className="flex h-full w-full min-h-[200px] flex-col items-center justify-center rounded-xl border border-border bg-card p-6 text-center shadow-sm">
          <div className="mb-4 rounded-full bg-warning/10 p-3">
            <AlertTriangle className="h-8 w-8 text-warning" />
          </div>
          <h2 className="text-lg font-semibold mb-1">Failed to load {this.props.moduleName}</h2>
          <p className="text-sm text-muted-foreground mb-6 max-w-md">
            An unexpected error occurred while rendering this module. You can try reloading just this section.
          </p>
          <button
            onClick={this.resetError}
            className="inline-flex items-center gap-2 rounded-md bg-secondary px-4 py-2 text-sm font-medium text-secondary-foreground shadow-sm hover:bg-secondary/80 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
          >
            <RefreshCw className="h-4 w-4" />
            Try Again
          </button>
        </div>
      )
    }

    return this.props.children
  }
}
