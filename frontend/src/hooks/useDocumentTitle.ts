import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { NAVIGATION_CONFIG } from '@/constants/navigation'

export function useDocumentTitle() {
  const { pathname } = useLocation()

  useEffect(() => {
    let title = 'NeoFactory'

    // Find the current page title
    for (const group of NAVIGATION_CONFIG) {
      for (const item of group.items) {
        if (item.href === pathname) {
          title = `${item.label} | NeoFactory`
          break
        }
      }
    }

    document.title = title
  }, [pathname])
}
