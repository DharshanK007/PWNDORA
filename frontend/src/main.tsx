import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@/styles/globals.css'
import App from './App'

// ─── Application Entry Point ──────────────────────────────────────────────────

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error('[NeoFactory] Root element not found. Ensure index.html has <div id="root" />.')
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>
)
