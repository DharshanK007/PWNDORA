import type { ReactNode } from 'react'
import { AppLogo } from '@/components/common/AppLogo'
import { APP } from '@/constants/app'
import { LabStatusBar } from '@/components/lab/LabStatusBar'

// ─── Auth Layout ──────────────────────────────────────────────────────────────
// Centered card layout for login and auth pages

interface AuthLayoutProps {
  children: ReactNode
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col bg-muted/30 relative">
      <LabStatusBar />
      <div className="flex-1 flex flex-col items-center justify-center p-4">
        {/* Logo */}
        <div className="mb-8 flex flex-col items-center gap-3">
        <AppLogo />
        <p className="text-xs text-muted-foreground">{APP.DESCRIPTION}</p>
      </div>

      {/* Card */}
      <div className="w-full max-w-md rounded-2xl border border-border bg-card p-8 shadow-lg">
        {children}
      </div>

      {/* Footer */}
      <p className="mt-6 text-xs text-muted-foreground">
        © {new Date().getFullYear()} {APP.COMPANY}. All rights reserved.
      </p>
      </div>
    </div>
  )
}
