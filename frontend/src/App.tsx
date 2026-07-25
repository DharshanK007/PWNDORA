import { AppProviders } from '@/components/providers/AppProviders'
import { AppRoutes } from '@/routes'
import { LabStatusBar } from '@/components/lab/LabStatusBar'

// ─── Root Application ─────────────────────────────────────────────────────────

function App() {
  return (
    <AppProviders>
      <div className="flex flex-col h-screen overflow-hidden">
        <div className="flex-1 overflow-y-auto relative flex flex-col">
          <AppRoutes />
        </div>
      </div>
    </AppProviders>
  )
}

export default App
