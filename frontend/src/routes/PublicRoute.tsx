import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { ROUTES } from '@/constants/routes'
import { LoadingPage } from '@/components/common/LoadingPage'

// ─── Public Route ─────────────────────────────────────────────────────────────

export function PublicRoute() {
  const { isAuthenticated, isInitializing } = useAuth()

  if (isInitializing) {
    return <LoadingPage message="Restoring session…" />
  }

  if (isAuthenticated) {
    return <Navigate to={ROUTES.DASHBOARD} replace />
  }

  return <Outlet />
}
