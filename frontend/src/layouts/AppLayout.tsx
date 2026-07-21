import { Outlet } from 'react-router-dom'
import { Navbar } from '@/components/layout/Navbar'
import { Sidebar } from '@/components/layout/Sidebar'
import { MobileSidebar } from '@/components/layout/MobileSidebar'
import { BreadcrumbBar } from '@/components/layout/BreadcrumbBar'
import { Footer } from '@/components/layout/Footer'
import { useSidebar } from '@/hooks/useSidebar'
import { useDocumentTitle } from '@/hooks/useDocumentTitle'

export function AppLayout() {
  const { isCollapsed, isMobileOpen, toggleCollapsed, toggleMobile, closeMobile } = useSidebar()
  
  // Automatically manage document title based on route
  useDocumentTitle()

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* Desktop Sidebar */}
      <Sidebar collapsed={isCollapsed} onToggle={toggleCollapsed} />
      
      {/* Mobile Sidebar (Drawer) */}
      <MobileSidebar isOpen={isMobileOpen} onClose={closeMobile} />

      {/* Main Content Area */}
      <div className="flex flex-1 flex-col overflow-hidden relative">
        {/* Navbar */}
        <Navbar onMenuClick={toggleMobile} />
        
        {/* Breadcrumb Bar */}
        <BreadcrumbBar />

        {/* Page Content */}
        <main
          id="main-content"
          className="flex-1 overflow-y-auto bg-muted/20"
        >
          <div className="mx-auto max-w-7xl p-4 md:p-6 lg:p-8 animate-fade-in min-h-full flex flex-col">
            <Outlet />
          </div>
        </main>

        {/* Footer */}
        <Footer />
      </div>
    </div>
  )
}
