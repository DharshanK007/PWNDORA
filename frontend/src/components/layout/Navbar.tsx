import { Menu } from 'lucide-react'
import { AppLogo } from '@/components/common/AppLogo'
import { SearchBar } from './SearchBar'
import { NotificationMenu } from './NotificationMenu'
import { UserMenu } from './UserMenu'

interface NavbarProps {
  onMenuClick: () => void
}

export function Navbar({ onMenuClick }: NavbarProps) {
  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b border-border bg-card px-4 shadow-sm relative z-10">
      {/* Left: Menu toggle + Logo (mobile only) */}
      <div className="flex items-center gap-3 lg:w-1/3">
        <button
          id="sidebar-toggle"
          onClick={onMenuClick}
          aria-label="Toggle menu"
          className="rounded-md p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
        >
          <Menu className="h-5 w-5" />
        </button>
        <div className="md:hidden">
          <AppLogo />
        </div>
      </div>

      {/* Center: Search Bar */}
      <div className="hidden md:flex flex-1 items-center justify-center lg:w-1/3">
        <SearchBar />
      </div>

      {/* Right: Actions */}
      <div className="flex flex-1 items-center justify-end gap-2 lg:w-1/3">
        <NotificationMenu />
        <div className="h-6 w-px bg-border mx-1"></div>
        <UserMenu />
      </div>
    </header>
  )
}
