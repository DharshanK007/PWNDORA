import { AppProviders } from '@/components/providers/AppProviders'
import { AppRoutes } from '@/routes'

// ─── Root Application ─────────────────────────────────────────────────────────

function App() {
  return (
    <AppProviders>
      <AppRoutes />
    </AppProviders>
  )
}

export default App
