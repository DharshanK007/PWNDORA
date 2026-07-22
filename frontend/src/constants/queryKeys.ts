export const QUERY_KEYS = {
  // Enterprise
  DASHBOARD: 'enterprise/dashboard',
  EMPLOYEES: 'enterprise/employees',
  EMPLOYEE: 'enterprise/employee',
  DEPARTMENTS: 'enterprise/departments',
  DEPARTMENT: 'enterprise/department',
  ASSETS: 'enterprise/assets',
  ASSET: 'enterprise/asset',
  NETWORK: 'enterprise/network',
  MAINTENANCE: 'enterprise/maintenance',
  TICKET: 'enterprise/ticket',
  USERS: 'enterprise/users',
  USER: 'enterprise/user',
  ROLES: 'enterprise/roles',
  REPORTS: 'enterprise/reports',
  REPORT: 'enterprise/report',
  
  // Scenarios
  SCENARIOS: 'scenario/list',
  SCENARIO: 'scenario/detail',
  SCENARIO_PROGRESS: 'scenario/progress',
  SCENARIO_CATEGORIES: 'scenario/categories',
  RECENT_SCENARIOS: 'scenario/recent',
  RECOMMENDED_SCENARIOS: 'scenario/recommended',

  // Session / Workspace
  SESSION: 'session/current',
  WORKSPACE: 'workspace/state',
} as const
