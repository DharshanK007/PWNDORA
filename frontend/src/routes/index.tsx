import { lazy, Suspense, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ROUTES } from '@/constants/routes'
import { useAuth } from '@/hooks/useAuth'

// ─── Layouts & Components ──────────────────────────────────────────────────────
import { AppLayout } from '@/layouts/AppLayout'
import { LoadingPage } from '@/components/common/LoadingPage'
import { PageErrorBoundary } from '@/components/error/PageErrorBoundary'

// ─── Guards ───────────────────────────────────────────────────────────────────
import { ProtectedRoute } from '@/routes/ProtectedRoute'
import { PublicRoute } from '@/routes/PublicRoute'

// ─── Eagerly Loaded Pages (Critical Path) ─────────────────────────────────────
import { LoginPage } from '@/pages/auth/LoginPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

// ─── Skeletons ────────────────────────────────────────────────────────────────
import { DashboardSkeleton } from '@/components/skeleton/DashboardSkeleton'
import { ScenarioCatalogSkeleton } from '@/components/skeleton/ScenarioCatalogSkeleton'

// ─── Lazy Loaded Pages ────────────────────────────────────────────────────────
const DashboardPage = lazy(() => import('@/pages/dashboard/DashboardPage').then(m => ({ default: m.DashboardPage })))
const EmployeesPage = lazy(() => import('@/pages/employees/EmployeesPage').then(m => ({ default: m.EmployeesPage })))
const DepartmentsPage = lazy(() => import('@/pages/departments/DepartmentsPage').then(m => ({ default: m.DepartmentsPage })))
const AssetsPage = lazy(() => import('@/pages/assets/AssetsPage').then(m => ({ default: m.AssetsPage })))
const NetworkPage = lazy(() => import('@/pages/network/NetworkPage').then(m => ({ default: m.NetworkPage })))
const MaintenancePage = lazy(() => import('@/pages/maintenance/MaintenancePage').then(m => ({ default: m.MaintenancePage })))
const ReportsPage = lazy(() => import('@/pages/reports/ReportsPage').then(m => ({ default: m.ReportsPage })))
const ScenarioCatalogPage = lazy(() => import('@/pages/scenarios/ScenarioCatalogPage').then(m => ({ default: m.ScenarioCatalogPage })))
const ScenarioDetailsPage = lazy(() => import('@/pages/scenarios/ScenarioDetailsPage').then(m => ({ default: m.ScenarioDetailsPage })))
const ProfilePage = lazy(() => import('@/pages/profile/ProfilePage').then(m => ({ default: m.ProfilePage })))
const SettingsPage = lazy(() => import('@/pages/settings/SettingsPage').then(m => ({ default: m.SettingsPage })))
const WelcomePage = lazy(() => import('@/pages/welcome/WelcomePage').then(m => ({ default: m.WelcomePage })))

// New Placeholders (Default exports)
const ReplayPage = lazy(() => import('@/pages/replay/ReplayPage'))
const MonitoringPage = lazy(() => import('@/pages/monitoring/MonitoringPage'))
const AuditLogsPage = lazy(() => import('@/pages/audit-logs/AuditLogsPage'))
const UsersPage = lazy(() => import('@/pages/users/UsersPage').then(m => ({ default: m.UsersPage })))
const RolesPage = lazy(() => import('@/pages/roles/RolesPage').then(m => ({ default: m.RolesPage })))

// ─── Preloading Hook ──────────────────────────────────────────────────────────
function useRoutePreload() {
  const { isAuthenticated } = useAuth()
  
  useEffect(() => {
    if (isAuthenticated) {
      // Preload high-traffic routes immediately after login
      import('@/pages/dashboard/DashboardPage')
      import('@/pages/scenarios/ScenarioCatalogPage')
    }
  }, [isAuthenticated])
}

// ─── App Router ───────────────────────────────────────────────────────────────

export function AppRoutes() {
  useRoutePreload()

  return (
    <Routes>
      {/* ── Root Landing / Welcome ── */}
      <Route path={ROUTES.HOME} element={<Suspense fallback={<LoadingPage />}><WelcomePage /></Suspense>} />

      {/* ── Auth routes ── */}
      <Route element={<PublicRoute />}>
        <Route path={ROUTES.LOGIN} element={<Suspense fallback={<LoadingPage />}><LoginPage /></Suspense>} />
      </Route>

      {/* ── Enterprise routes (sidebar layout) ── */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          {/* Enterprise */}
          <Route path={ROUTES.DASHBOARD} element={
            <PageErrorBoundary>
              <Suspense fallback={<DashboardSkeleton />}>
                <DashboardPage />
              </Suspense>
            </PageErrorBoundary>
          } />
          
          <Route path={ROUTES.EMPLOYEES} element={<Suspense fallback={<LoadingPage />}><EmployeesPage /></Suspense>} />
          <Route path={ROUTES.DEPARTMENTS} element={<Suspense fallback={<LoadingPage />}><DepartmentsPage /></Suspense>} />
          <Route path={ROUTES.ASSETS} element={<Suspense fallback={<LoadingPage />}><AssetsPage /></Suspense>} />
          <Route path={ROUTES.NETWORK} element={<Suspense fallback={<LoadingPage />}><NetworkPage /></Suspense>} />
          <Route path={ROUTES.MAINTENANCE} element={<Suspense fallback={<LoadingPage />}><MaintenancePage /></Suspense>} />
          
          {/* Cyber Range */}
          <Route path={ROUTES.SCENARIOS} element={
            <PageErrorBoundary>
              <Suspense fallback={<ScenarioCatalogSkeleton />}>
                <ScenarioCatalogPage />
              </Suspense>
            </PageErrorBoundary>
          } />
          <Route path={ROUTES.SCENARIO_DETAIL} element={<Suspense fallback={<LoadingPage />}><ScenarioDetailsPage /></Suspense>} />

          <Route path={ROUTES.REPLAY} element={<Suspense fallback={<LoadingPage />}><ReplayPage /></Suspense>} />

          {/* Analytics */}
          <Route path={ROUTES.REPORTS} element={<Suspense fallback={<LoadingPage />}><ReportsPage /></Suspense>} />
          <Route path={ROUTES.MONITORING} element={<Suspense fallback={<LoadingPage />}><MonitoringPage /></Suspense>} />
          <Route path={ROUTES.AUDIT_LOGS} element={<Suspense fallback={<LoadingPage />}><AuditLogsPage /></Suspense>} />

          {/* Administration */}
          <Route path={ROUTES.USERS} element={<Suspense fallback={<LoadingPage />}><UsersPage /></Suspense>} />
          <Route path={ROUTES.ROLES} element={<Suspense fallback={<LoadingPage />}><RolesPage /></Suspense>} />

          {/* User */}
          <Route path={ROUTES.PROFILE} element={<Suspense fallback={<LoadingPage />}><ProfilePage /></Suspense>} />
          <Route path={ROUTES.SETTINGS} element={<Suspense fallback={<LoadingPage />}><SettingsPage /></Suspense>} />
        </Route>
      </Route>

      {/* ── 404 ── */}
      <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
    </Routes>
  )
}
