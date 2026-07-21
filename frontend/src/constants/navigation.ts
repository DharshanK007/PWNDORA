import {
  LayoutDashboard,
  Users,
  Building2,
  MonitorSpeaker,
  Network,
  Wrench,
  FileBarChart2,
  ShieldAlert,
  Search,
  Settings,
  UserCircle,
  PlaySquare,
  Activity,
  ClipboardList,
  UserCog,
  ShieldCheck,
} from 'lucide-react'
import { ROUTES } from './routes'
import type { NavGroup } from '@/types/navigation'

export const NAVIGATION_CONFIG: NavGroup[] = [
  {
    id: 'dashboard-group',
    label: 'Dashboard',
    items: [
      {
        id: 'dashboard',
        label: 'Dashboard',
        href: ROUTES.DASHBOARD,
        icon: LayoutDashboard,
      },
    ],
  },
  {
    id: 'enterprise-group',
    label: 'Enterprise',
    items: [
      {
        id: 'employees',
        label: 'Employees',
        href: ROUTES.EMPLOYEES,
        icon: Users,
      },
      {
        id: 'departments',
        label: 'Departments',
        href: ROUTES.DEPARTMENTS,
        icon: Building2,
      },
      {
        id: 'assets',
        label: 'Assets',
        href: ROUTES.ASSETS,
        icon: MonitorSpeaker,
      },
      {
        id: 'network',
        label: 'Network',
        href: ROUTES.NETWORK,
        icon: Network,
      },
      {
        id: 'maintenance',
        label: 'Maintenance',
        href: ROUTES.MAINTENANCE,
        icon: Wrench,
      },
    ],
  },
  {
    id: 'cyber-range-group',
    label: 'Cyber Range',
    items: [
      {
        id: 'scenarios',
        label: 'Scenarios',
        href: ROUTES.SCENARIOS,
        icon: ShieldAlert,
      },
      {
        id: 'investigation',
        label: 'Investigation',
        href: ROUTES.INVESTIGATION,
        icon: Search,
      },
      {
        id: 'replay',
        label: 'Replay',
        href: ROUTES.REPLAY,
        icon: PlaySquare,
      },
    ],
  },
  {
    id: 'analytics-group',
    label: 'Analytics',
    items: [
      {
        id: 'reports',
        label: 'Reports',
        href: ROUTES.REPORTS,
        icon: FileBarChart2,
      },
      {
        id: 'monitoring',
        label: 'Monitoring',
        href: ROUTES.MONITORING,
        icon: Activity,
      },
      {
        id: 'audit-logs',
        label: 'Audit Logs',
        href: ROUTES.AUDIT_LOGS,
        icon: ClipboardList,
      },
    ],
  },
  {
    id: 'administration-group',
    label: 'Administration',
    items: [
      {
        id: 'settings',
        label: 'Settings',
        href: ROUTES.SETTINGS,
        icon: Settings,
      },
      {
        id: 'users',
        label: 'Users',
        href: ROUTES.USERS,
        icon: UserCog,
      },
      {
        id: 'roles',
        label: 'Roles',
        href: ROUTES.ROLES,
        icon: ShieldCheck,
      },
    ],
  },
]

export const BOTTOM_NAVIGATION_CONFIG = [
  {
    id: 'profile',
    label: 'Profile',
    href: ROUTES.PROFILE,
    icon: UserCircle,
  },
]
