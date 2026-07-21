import { useEffect } from 'react'
import { X } from 'lucide-react'
import { AppLogo } from '@/components/common/AppLogo'
import { NAVIGATION_CONFIG, BOTTOM_NAVIGATION_CONFIG } from '@/constants/navigation'
import { SidebarGroup } from './SidebarGroup'
import { SidebarItem } from './SidebarItem'
import { cn } from '@/lib/utils'

interface MobileSidebarProps {
  isOpen: boolean
  onClose: () => void
}

export function MobileSidebar({ isOpen, onClose }: MobileSidebarProps) {
  // Lock body scroll when drawer is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [isOpen])

  // Handle escape key
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) onClose()
    }
    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [isOpen, onClose])

  return (
    <>
      {/* Overlay */}
      <div
        className={cn(
          'fixed inset-0 z-40 bg-background/80 backdrop-blur-sm transition-all duration-300 md:hidden',
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        )}
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex w-3/4 max-w-sm flex-col bg-sidebar border-r border-sidebar-border shadow-2xl transition-transform duration-300 ease-in-out md:hidden',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
        role="dialog"
        aria-modal="true"
        aria-label="Mobile Navigation"
      >
        <div className="flex h-14 items-center justify-between border-b border-sidebar-border px-4 shrink-0">
          <AppLogo />
          <button
            onClick={onClose}
            aria-label="Close menu"
            className="rounded-md p-1.5 text-sidebar-foreground/50 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-6 custom-scrollbar">
          {NAVIGATION_CONFIG.map(group => (
            <SidebarGroup key={group.id} group={group} collapsed={false} />
          ))}
        </nav>

        <div className="border-t border-sidebar-border px-3 py-4 space-y-1 shrink-0">
          {BOTTOM_NAVIGATION_CONFIG.map(item => (
            <SidebarItem key={item.id} item={item} collapsed={false} />
          ))}
        </div>
      </aside>
    </>
  )
}
