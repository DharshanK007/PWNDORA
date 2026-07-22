import { WifiOff, RefreshCcw } from 'lucide-react'

interface NetworkErrorProps {
  onRetry: () => void
  message?: string
}

export function NetworkError({ onRetry, message = 'We are having trouble connecting to the server. Please check your internet connection.' }: NetworkErrorProps) {
  return (
    <div className="flex min-h-[400px] w-full flex-col items-center justify-center p-6 text-center">
      <div className="mb-6 rounded-full bg-muted p-6">
        <WifiOff className="h-12 w-12 text-muted-foreground" />
      </div>
      <h2 className="mb-2 text-2xl font-bold tracking-tight text-foreground">Connection Error</h2>
      <p className="mb-8 max-w-[400px] text-muted-foreground">
        {message}
      </p>
      <button
        onClick={onRetry}
        className="inline-flex items-center gap-2 rounded-md bg-primary px-6 py-2.5 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
      >
        <RefreshCcw className="h-4 w-4" />
        Try Again
      </button>
    </div>
  )
}
