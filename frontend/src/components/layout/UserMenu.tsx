import { useState, useRef, useEffect } from 'react'
import { ChevronDown, LogOut, User as UserIcon, Settings, Moon, Sun, Monitor } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { useTheme } from '@/hooks/useTheme'
import { getInitials } from '@/utils/helpers'
import { THEMES, type Theme } from '@/constants/app'
import { cn } from '@/lib/utils'

const themeIcons: Record<Theme, typeof Sun> = {
  light: Sun,
  dark: Moon,
  system: Monitor,
}

export function UserMenu() {
  const { user, logout } = useAuth()
  const { theme, setTheme } = useTheme()
  const [open, setOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div ref={menuRef} className="relative ml-1">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 rounded-md p-1 hover:bg-muted transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
      >
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground select-none">
          {user ? getInitials(user.email.split('@')[0]) : 'U'}
        </div>
        <div className="hidden flex-col items-start text-left md:flex">
          <span className="text-xs font-medium leading-none text-foreground">
            {user ? user.email.split('@')[0] : 'User'}
          </span>
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground mt-0.5">
            {user ? user.role : 'Role'}
          </span>
        </div>
        <ChevronDown className={cn(
          'h-3.5 w-3.5 text-muted-foreground transition-transform',
          open ? 'rotate-180' : ''
        )} />
      </button>

      {open && (
        <div className="absolute right-0 top-full z-50 mt-1 w-56 rounded-lg border border-border bg-popover shadow-lg py-1 animate-fade-in">
          <div className="px-3 py-2 border-b border-border mb-1 md:hidden">
            <p className="text-sm font-medium text-foreground">{user?.email}</p>
            <p className="text-xs text-muted-foreground mt-0.5">{user?.role}</p>
          </div>

          <div className="px-1 py-1">
            <button className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm text-popover-foreground hover:bg-accent transition-colors">
              <UserIcon className="h-4 w-4" />
              Profile
            </button>
            <button className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm text-popover-foreground hover:bg-accent transition-colors">
              <Settings className="h-4 w-4" />
              Settings
            </button>
          </div>

          <div className="border-t border-border px-1 py-1">
            <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Theme
            </div>
            {THEMES.map(t => {
              const Icon = themeIcons[t]
              return (
                <button
                  key={t}
                  onClick={() => { setTheme(t); setOpen(false) }}
                  className={cn(
                    'flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors',
                    theme === t
                      ? 'bg-accent text-accent-foreground font-medium'
                      : 'text-popover-foreground hover:bg-accent'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              )
            })}
          </div>

          <div className="border-t border-border px-1 py-1">
            <button
              onClick={() => {
                setOpen(false)
                logout()
              }}
              className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm text-destructive hover:bg-destructive/10 transition-colors"
            >
              <LogOut className="h-4 w-4" />
              Sign Out
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
