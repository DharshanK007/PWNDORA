import { ChevronLeft, ChevronRight } from 'lucide-react'
import { AppLogo } from '@/components/common/AppLogo'
import { NAVIGATION_CONFIG, BOTTOM_NAVIGATION_CONFIG } from '@/constants/navigation'
import { SidebarGroup } from './SidebarGroup'
import { SidebarItem } from './SidebarItem'
import { cn } from '@/lib/utils'

interface SidebarProps {
  collapsed: boolean
  onToggle: () => void
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  return (
    <aside
      id="app-sidebar"
      className={cn(
        'hidden md:flex flex-col border-r border-sidebar-border bg-sidebar transition-all duration-300 ease-in-out',
        collapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Logo Area */}
      <div
        className={cn(
          'flex h-14 items-center border-b border-sidebar-border px-4 shrink-0',
          collapsed ? 'justify-center' : 'justify-between'
        )}
      >
        <AppLogo collapsed={collapsed} />
        {!collapsed && (
          <button
            onClick={onToggle}
            aria-label="Collapse sidebar"
            className="rounded-md p-1.5 text-sidebar-foreground/50 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Expand button when collapsed */}
      {collapsed && (
        <button
          onClick={onToggle}
          aria-label="Expand sidebar"
          className="mx-auto mt-3 rounded-md p-1.5 text-sidebar-foreground/50 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
        >
          <ChevronRight className="h-4 w-4" />
        </button>
      )}

      {/* Main Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-6 custom-scrollbar">
        {NAVIGATION_CONFIG.map(group => (
          <SidebarGroup key={group.id} group={group} collapsed={collapsed} />
        ))}
      </nav>

      {/* Bottom Navigation */}
      <div className="border-t border-sidebar-border px-3 py-4 space-y-1 shrink-0">
        {BOTTOM_NAVIGATION_CONFIG.map(item => (
          <SidebarItem key={item.id} item={item} collapsed={collapsed} />
        ))}
      </div>
    </aside>
  )
}
