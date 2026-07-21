import { useState, useEffect } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'
import { useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import type { NavGroup } from '@/types/navigation'
import { SidebarItem } from './SidebarItem'

interface SidebarGroupProps {
  group: NavGroup
  collapsed: boolean
}

export function SidebarGroup({ group, collapsed }: SidebarGroupProps) {
  const { pathname } = useLocation()
  
  // Auto-expand if the active route is in this group
  const isActiveGroup = group.items.some(item => item.href === pathname)
  const [isExpanded, setIsExpanded] = useState(isActiveGroup || group.id === 'dashboard-group')

  // Re-evaluate auto-expand when route changes
  useEffect(() => {
    if (isActiveGroup && !isExpanded) {
      setIsExpanded(true)
    }
  }, [isActiveGroup, isExpanded])

  // Top level groups like Dashboard without many items don't need a collapsible header
  const isSingleItem = group.items.length === 1 && group.items[0].label === group.label

  if (isSingleItem) {
    return (
      <div className="space-y-1">
        <SidebarItem item={group.items[0]} collapsed={collapsed} />
      </div>
    )
  }

  return (
    <div className="space-y-1">
      {!collapsed && (
        <button
          onClick={() => setIsExpanded(prev => !prev)}
          className="flex w-full items-center justify-between px-3 py-2 text-xs font-semibold uppercase tracking-wider text-sidebar-foreground/50 hover:text-sidebar-foreground transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary rounded-md"
        >
          {group.label}
          {isExpanded ? (
            <ChevronDown className="h-3.5 w-3.5 transition-transform" />
          ) : (
            <ChevronRight className="h-3.5 w-3.5 transition-transform" />
          )}
        </button>
      )}

      {/* Render children if expanded or collapsed (if collapsed, we just show them without the header) */}
      <div
        className={cn(
          'space-y-1 overflow-hidden transition-all duration-300 ease-in-out',
          !collapsed && !isExpanded ? 'max-h-0 opacity-0' : 'max-h-[500px] opacity-100',
          collapsed && 'mt-4' // Space out groups when collapsed
        )}
      >
        {group.items.map(item => (
          <SidebarItem key={item.id} item={item} collapsed={collapsed} />
        ))}
      </div>
    </div>
  )
}
