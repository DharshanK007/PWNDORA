import { cn } from '@/lib/utils'

// ─── Loading Spinner ──────────────────────────────────────────────────────────

type SpinnerSize = 'sm' | 'md' | 'lg' | 'xl'

const sizeClasses: Record<SpinnerSize, string> = {
  sm: 'h-4 w-4 border-2',
  md: 'h-6 w-6 border-2',
  lg: 'h-8 w-8 border-[3px]',
  xl: 'h-12 w-12 border-4',
}

interface LoadingSpinnerProps {
  size?: SpinnerSize
  className?: string
  'aria-label'?: string
}

export function LoadingSpinner({
  size = 'md',
  className,
  'aria-label': ariaLabel = 'Loading',
}: LoadingSpinnerProps) {
  return (
    <div
      role="status"
      aria-label={ariaLabel}
      className={cn(
        'animate-spin rounded-full border-current border-t-transparent text-primary',
        sizeClasses[size],
        className
      )}
    />
  )
}
