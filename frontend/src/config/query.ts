import { QueryClient } from '@tanstack/react-query'

// ─── Default Query Configuration ─────────────────────────────────────────────

export const queryClientConfig = {
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,        // 5 minutes
      gcTime: 1000 * 60 * 10,          // 10 minutes garbage collection
      retry: 2,
      retryDelay: (attemptIndex: number) => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
}

// ─── Singleton QueryClient ────────────────────────────────────────────────────

export const queryClient = new QueryClient(queryClientConfig)
