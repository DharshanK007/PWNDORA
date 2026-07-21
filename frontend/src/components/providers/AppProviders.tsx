import type { ReactNode } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { AuthProvider } from '@/contexts/AuthContext'
import { ThemeProvider } from '@/contexts/ThemeContext'
import { ErrorBoundary } from '@/components/feedback/ErrorBoundary'
import { queryClient } from '@/config/query'
import { env } from '@/config/env'

// ─── App Providers ────────────────────────────────────────────────────────────
// All global providers composed in a single wrapper.
// Order matters: Router → Query → Theme → Auth → ErrorBoundary

interface AppProvidersProps {
  children: ReactNode
}

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider defaultTheme="system">
          <AuthProvider>
            <ErrorBoundary>
              {children}
            </ErrorBoundary>
          </AuthProvider>
        </ThemeProvider>
        {env.IS_DEV && <ReactQueryDevtools initialIsOpen={false} />}
      </QueryClientProvider>
    </BrowserRouter>
  )
}
