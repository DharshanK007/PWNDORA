/* eslint-disable react-refresh/only-export-components */
import { createContext, useEffect, useState, useCallback, type ReactNode } from 'react'
import { STORAGE_KEYS, type Theme } from '@/constants/app'

// ─── Theme Context Type ───────────────────────────────────────────────────────

export interface ThemeContextValue {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
}

// ─── Context ──────────────────────────────────────────────────────────────────

export const ThemeContext = createContext<ThemeContextValue | null>(null)

// ─── Provider ─────────────────────────────────────────────────────────────────

interface ThemeProviderProps {
  children: ReactNode
  defaultTheme?: Theme
}

export function ThemeProvider({ children, defaultTheme = 'system' }: ThemeProviderProps) {
  const [theme, setThemeState] = useState<Theme>(() => {
    const stored = localStorage.getItem(STORAGE_KEYS.THEME) as Theme | null
    return stored ?? defaultTheme
  })

  const resolvedTheme: 'light' | 'dark' =
    theme === 'system'
      ? window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
      : theme

  // Apply class to <html>
  useEffect(() => {
    const root = document.documentElement
    root.classList.remove('light', 'dark')
    root.classList.add(resolvedTheme)
  }, [resolvedTheme])

  // Listen for system theme changes
  useEffect(() => {
    if (theme !== 'system') return
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = () => {
      const root = document.documentElement
      root.classList.remove('light', 'dark')
      root.classList.add(media.matches ? 'dark' : 'light')
    }
    media.addEventListener('change', handleChange)
    return () => media.removeEventListener('change', handleChange)
  }, [theme])

  const setTheme = useCallback((newTheme: Theme) => {
    localStorage.setItem(STORAGE_KEYS.THEME, newTheme)
    setThemeState(newTheme)
  }, [])

  const value: ThemeContextValue = { theme, setTheme, resolvedTheme }

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}


