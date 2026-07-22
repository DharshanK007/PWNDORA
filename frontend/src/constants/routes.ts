// ─── Application Route Constants ──────────────────────────────────────────────
// Use these constants everywhere instead of string literals.

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',

  // ── Enterprise Modules ──
  DASHBOARD: '/dashboard',
  EMPLOYEES: '/employees',
  DEPARTMENTS: '/departments',
  ASSETS: '/assets',
  NETWORK: '/network',
  MAINTENANCE: '/maintenance',

  // ── Cyber Range ──
  SCENARIOS: '/scenarios',
  SCENARIO_DETAIL: '/scenarios/:id',
  REPLAY: '/replay',

  // ── Analytics ──
  REPORTS: '/reports',
  MONITORING: '/monitoring',
  AUDIT_LOGS: '/audit-logs',

  // ── Administration ──
  USERS: '/users',
  ROLES: '/roles',

  // ── User ──
  PROFILE: '/profile',
  SETTINGS: '/settings',

  // ── Fallback ──
  NOT_FOUND: '/*',
} as const

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES]

// Helper to build dynamic paths
export const buildRoute = {
  scenarioDetail: (id: string) => `/scenarios/${id}`,
}
