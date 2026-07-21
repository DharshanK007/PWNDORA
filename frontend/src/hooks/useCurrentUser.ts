import { useQuery } from '@tanstack/react-query'
import { authService } from '@/services/auth'
import type { UserResponse } from '@/types/user'
import type { ApiError } from '@/types/api'

// ─── Query Key ────────────────────────────────────────────────────────────────

export const CURRENT_USER_QUERY_KEY = ['currentUser'] as const

// ─── Hook ─────────────────────────────────────────────────────────────────────

export function useCurrentUser(enabled: boolean) {
  return useQuery<UserResponse, ApiError>({
    queryKey: CURRENT_USER_QUERY_KEY,
    queryFn: authService.getCurrentUser,
    enabled,
    staleTime: 1000 * 60 * 15, // 15 minutes
    retry: false, // Don't retry on 401
  })
}
