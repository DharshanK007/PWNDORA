import type { LucideIcon } from 'lucide-react'
import type { AppRoute } from '@/constants/routes'

export interface NavItem {
  id: string
  label: string
  href?: AppRoute | string
  icon?: LucideIcon
  children?: NavItem[]
  disabled?: boolean
}

export interface NavGroup {
  id: string
  label: string
  items: NavItem[]
}

export interface Breadcrumb {
  label: string
  href?: string
}
