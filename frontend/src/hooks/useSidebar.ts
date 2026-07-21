import { useState, useCallback, useEffect } from 'react'
import { STORAGE_KEYS } from '@/constants/app'

export function useSidebar() {
  // Desktop sidebar collapsed state
  const [isCollapsed, setIsCollapsed] = useState(() => {
    return localStorage.getItem(STORAGE_KEYS.SIDEBAR_COLLAPSED) === 'true'
  })

  // Mobile drawer open state
  const [isMobileOpen, setIsMobileOpen] = useState(false)

  const toggleCollapsed = useCallback(() => {
    setIsCollapsed(prev => {
      const next = !prev
      localStorage.setItem(STORAGE_KEYS.SIDEBAR_COLLAPSED, String(next))
      return next
    })
  }, [])

  const toggleMobile = useCallback(() => {
    setIsMobileOpen(prev => !prev)
  }, [])

  const closeMobile = useCallback(() => {
    setIsMobileOpen(false)
  }, [])

  // Close mobile drawer on resize to desktop
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768 && isMobileOpen) {
        setIsMobileOpen(false)
      }
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [isMobileOpen])

  return {
    isCollapsed,
    isMobileOpen,
    toggleCollapsed,
    toggleMobile,
    closeMobile,
  }
}
