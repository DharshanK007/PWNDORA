import { lazy, Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ROUTES } from '@/constants/routes'

// ─── Layouts & Components ──────────────────────────────────────────────────────
import { AppLayout } from '@/layouts/AppLayout'
import { LoadingPage } from '@/components/common/LoadingPage'

// ─── Guards ───────────────────────────────────────────────────────────────────
import { ProtectedRoute } from '@/routes/ProtectedRoute'
import { PublicRoute } from '@/routes/PublicRoute'

// ─── Eagerly Loaded Pages (Critical Path) ─────────────────────────────────────
import { LoginPage } from '@/pages/auth/LoginPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

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
const InvestigationWorkspace = lazy(() => import('@/pages/workspace/InvestigationWorkspace').then(m => ({ default: m.InvestigationWorkspace })))
const ProfilePage = lazy(() => import('@/pages/profile/ProfilePage').then(m => ({ default: m.ProfilePage })))
const SettingsPage = lazy(() => import('@/pages/settings/SettingsPage').then(m => ({ default: m.SettingsPage })))

// New Placeholders (Default exports)
const ReplayPage = lazy(() => import('@/pages/replay/ReplayPage'))
const MonitoringPage = lazy(() => import('@/pages/monitoring/MonitoringPage'))
const AuditLogsPage = lazy(() => import('@/pages/audit-logs/AuditLogsPage'))
const UsersPage = lazy(() => import('@/pages/users/UsersPage').then(m => ({ default: m.UsersPage })))
const RolesPage = lazy(() => import('@/pages/roles/RolesPage').then(m => ({ default: m.RolesPage })))

// ─── App Router ───────────────────────────────────────────────────────────────

export function AppRoutes() {
  return (
    <Suspense fallback={<LoadingPage />}>
      <Routes>
        {/* ── Root redirect ── */}
        <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.DASHBOARD} replace />} />

        {/* ── Auth routes ── */}
        <Route element={<PublicRoute />}>
          <Route path={ROUTES.LOGIN} element={<LoginPage />} />
        </Route>

        {/* ── Enterprise routes (sidebar layout) ── */}
        <Route element={<ProtectedRoute />}>
          {/* Investigation Workspace (Own Fullscreen Layout) */}
          <Route path={ROUTES.INVESTIGATION} element={<InvestigationWorkspace />} />
          
          <Route element={<AppLayout />}>
            {/* Enterprise */}
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
            <Route path={ROUTES.EMPLOYEES} element={<EmployeesPage />} />
            <Route path={ROUTES.DEPARTMENTS} element={<DepartmentsPage />} />
            <Route path={ROUTES.ASSETS} element={<AssetsPage />} />
            <Route path={ROUTES.NETWORK} element={<NetworkPage />} />
            <Route path={ROUTES.MAINTENANCE} element={<MaintenancePage />} />
            
            {/* Cyber Range */}
            <Route path={ROUTES.SCENARIOS} element={<ScenarioCatalogPage />} />
            <Route path={ROUTES.SCENARIO_DETAIL} element={<ScenarioDetailsPage />} />

            <Route path={ROUTES.REPLAY} element={<ReplayPage />} />

            {/* Analytics */}
            <Route path={ROUTES.REPORTS} element={<ReportsPage />} />
            <Route path={ROUTES.MONITORING} element={<MonitoringPage />} />
            <Route path={ROUTES.AUDIT_LOGS} element={<AuditLogsPage />} />

            {/* Administration */}
            <Route path={ROUTES.USERS} element={<UsersPage />} />
            <Route path={ROUTES.ROLES} element={<RolesPage />} />

            {/* User */}
            <Route path={ROUTES.PROFILE} element={<ProfilePage />} />
            <Route path={ROUTES.SETTINGS} element={<SettingsPage />} />
          </Route>
        </Route>

        {/* ── 404 ── */}
        <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  )
}
