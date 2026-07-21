import { useMemo } from 'react'
import { useLocation } from 'react-router-dom'
import { NAVIGATION_CONFIG } from '@/constants/navigation'
import type { Breadcrumb } from '@/types/navigation'

export function useBreadcrumbs(): Breadcrumb[] {
  const { pathname } = useLocation()

  return useMemo(() => {
    // Basic match logic: Find the group and item that matches the current pathname
    for (const group of NAVIGATION_CONFIG) {
      for (const item of group.items) {
        if (item.href === pathname) {
          // If it's a top-level group like Dashboard, don't duplicate
          if (group.label === item.label) {
            return [{ label: group.label, href: item.href }]
          }

          // Return Group -> Item
          return [
            { label: 'Dashboard', href: '/' },
            { label: group.label },
            { label: item.label, href: item.href },
          ]
        }
      }
    }

    // Default fallback if no match is found (e.g., dynamic routes like /scenarios/:id)
    return [{ label: 'Dashboard', href: '/' }]
  }, [pathname])
}
