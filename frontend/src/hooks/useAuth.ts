import { useContext } from 'react'
import { AuthContext, type AuthContextValue } from '@/contexts/AuthContext'

// ─── useAuth Hook ─────────────────────────────────────────────────────────────

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within <AuthProvider>')
  }
  return ctx
}
