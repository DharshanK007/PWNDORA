/* eslint-disable react-refresh/only-export-components */
import { createContext, useEffect, useState, useCallback, useMemo, type ReactNode } from 'react'
import type { AuthState, Permission } from '@/types/auth'
import type { UserResponse } from '@/types/user'
import { tokenService } from '@/services/token'
import { AUTH_UNAUTHORIZED_EVENT } from '@/lib/axios'
import { useCurrentUser } from '@/hooks/useCurrentUser'
import { queryClient } from '@/config/query'

// ─── Auth Context Type ────────────────────────────────────────────────────────

export interface AuthContextValue extends AuthState {
  login: (token: string, user?: UserResponse) => void
  logout: () => void
}

// ─── Context ──────────────────────────────────────────────────────────────────

export const AuthContext = createContext<AuthContextValue | null>(null)

// ─── Provider ─────────────────────────────────────────────────────────────────

interface AuthProviderProps {
  children: ReactNode
}

import { authService } from '@/services/auth'
import { toast } from 'sonner'

export function AuthProvider({ children }: AuthProviderProps) {
  const [token, setToken] = useState<string | null>(tokenService.getAccessToken)
  const [user, setUser] = useState<UserResponse | null>(null)
  const [isAutoLoggingIn, setIsAutoLoggingIn] = useState(false)

  // Use TanStack Query to fetch current user if we have a token
  const { data: currentUserData, isLoading: isQueryLoading, isError } = useCurrentUser(!!token)

  // Derive initial session loading state. 
  // It's initializing if we have a token but haven't fetched the user yet, 
  // or if the query is currently loading, OR if we are currently auto-logging in.
  const isInitializing = (!!token && (!user && isQueryLoading)) || isAutoLoggingIn



  // Sync query data to local state when it arrives
  useEffect(() => {
    if (currentUserData) {
      setUser(currentUserData)
    }
  }, [currentUserData])

  const logout = useCallback(() => {
    tokenService.removeAccessToken()
    setToken(null)
    setUser(null)
    queryClient.clear() // Clear all query caches on logout
  }, [])

  // Auto-logout if the API returns 401
  useEffect(() => {
    if (isError) {
      logout()
    }
  }, [isError, logout])

  // Listen for global 401 events from Axios
  useEffect(() => {
    const handleUnauthorized = () => {
      logout()
    }
    window.addEventListener(AUTH_UNAUTHORIZED_EVENT, handleUnauthorized)
    return () => window.removeEventListener(AUTH_UNAUTHORIZED_EVENT, handleUnauthorized)
  }, [logout])

  const login = useCallback((newToken: string, newUser?: UserResponse) => {
    tokenService.setAccessToken(newToken)
    setToken(newToken)
    if (newUser) {
      setUser(newUser)
    }
  }, [])

  const value = useMemo<AuthContextValue>(
    () => {
      // Derive RBAC for the placeholder (can be expanded later)
      const roles = user ? [user.role] : []
      const permissions: Permission[] = [] // Empty for now, as requested

      return {
        user,
        token,
        isAuthenticated: !!token && !!user,
        isInitializing,
        roles,
        permissions,
        login,
        logout,
      }
    },
    [user, token, isInitializing, login, logout]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
