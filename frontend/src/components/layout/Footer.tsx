import { APP } from '@/constants/app'

// ─── Footer ───────────────────────────────────────────────────────────────────

export function Footer() {
  return (
    <footer className="flex h-10 items-center justify-between border-t border-border bg-card px-6">
      <p className="text-xs text-muted-foreground">
        © {new Date().getFullYear()} {APP.COMPANY}. All rights reserved.
      </p>
      <p className="text-xs text-muted-foreground">
        v{APP.VERSION}
      </p>
    </footer>
  )
}
