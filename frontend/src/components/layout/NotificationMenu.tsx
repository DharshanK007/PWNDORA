import { useState, useRef, useEffect } from 'react'
import { Bell, AlertCircle, Info, CheckCircle2 } from 'lucide-react'

export function NotificationMenu() {
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
    <div ref={menuRef} className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        aria-label="Notifications"
        className="relative rounded-md p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
      >
        <Bell className="h-5 w-5" />
        <span className="absolute right-1 top-1 flex h-2 w-2">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75"></span>
          <span className="relative inline-flex h-2 w-2 rounded-full bg-primary"></span>
        </span>
      </button>

      {open && (
        <div className="absolute right-0 top-full z-50 mt-1 w-80 rounded-lg border border-border bg-popover shadow-lg animate-fade-in overflow-hidden">
          <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-2">
            <h3 className="text-sm font-semibold text-foreground">Notifications</h3>
            <span className="text-[10px] font-medium text-muted-foreground">3 Unread</span>
          </div>
          <div className="max-h-80 overflow-y-auto p-2 space-y-1">
            <div className="flex items-start gap-3 rounded-md p-2 hover:bg-muted/50 transition-colors cursor-pointer">
              <AlertCircle className="mt-0.5 h-4 w-4 text-destructive shrink-0" />
              <div className="flex flex-col gap-1">
                <span className="text-sm font-medium leading-none">PLC-A1 offline</span>
                <span className="text-xs text-muted-foreground">The assembly line controller went offline unexpectedly.</span>
                <span className="text-[10px] text-muted-foreground">2 mins ago</span>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-md p-2 hover:bg-muted/50 transition-colors cursor-pointer">
              <CheckCircle2 className="mt-0.5 h-4 w-4 text-emerald-500 shrink-0" />
              <div className="flex flex-col gap-1">
                <span className="text-sm font-medium leading-none">Scenario completed</span>
                <span className="text-xs text-muted-foreground">User "alice" completed ransomware scenario.</span>
                <span className="text-[10px] text-muted-foreground">1 hr ago</span>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-md p-2 hover:bg-muted/50 transition-colors cursor-pointer">
              <Info className="mt-0.5 h-4 w-4 text-blue-500 shrink-0" />
              <div className="flex flex-col gap-1">
                <span className="text-sm font-medium leading-none">System Update</span>
                <span className="text-xs text-muted-foreground">NeoFactory v2.1 will be deployed at 00:00 UTC.</span>
                <span className="text-[10px] text-muted-foreground">3 hrs ago</span>
              </div>
            </div>
          </div>
          <div className="border-t border-border p-1">
            <button className="w-full rounded p-2 text-center text-xs font-medium text-primary hover:bg-muted transition-colors">
              View all notifications
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
