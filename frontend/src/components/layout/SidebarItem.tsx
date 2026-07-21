import { NavLink } from 'react-router-dom'
import { cn } from '@/lib/utils'
import type { NavItem } from '@/types/navigation'

interface SidebarItemProps {
  item: NavItem
  collapsed: boolean
}

export function SidebarItem({ item, collapsed }: SidebarItemProps) {
  if (!item.icon || !item.href) return null
  const Icon = item.icon

  return (
    <NavLink
      to={item.href}
      title={collapsed ? item.label : undefined}
      className={({ isActive }) =>
        cn(
          'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all duration-200 relative group',
          isActive
            ? 'bg-primary text-primary-foreground font-medium shadow-sm'
            : 'text-sidebar-foreground/80 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground',
          collapsed && 'justify-center px-2'
        )
      }
    >
      <Icon className="h-4 w-4 flex-shrink-0" />
      {!collapsed && <span>{item.label}</span>}
      
      {/* Tooltip for collapsed state */}
      {collapsed && (
        <div className="absolute left-full ml-2 hidden rounded-md bg-popover px-2 py-1 text-xs font-medium text-popover-foreground shadow-md group-hover:block z-50 animate-in fade-in zoom-in-95 duration-100">
          {item.label}
        </div>
      )}
    </NavLink>
  )
}
