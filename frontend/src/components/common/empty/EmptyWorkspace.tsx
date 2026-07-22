import { LayoutTemplate, Search } from 'lucide-react'
import { Link } from 'react-router-dom'
import { ROUTES } from '@/constants/routes'

export function EmptyWorkspace() {
  return (
    <div className="h-full w-full flex flex-col items-center justify-center bg-background text-foreground p-8 animate-in fade-in duration-500">
      <div className="w-20 h-20 border border-border bg-muted/30 rounded-xl mb-6 flex items-center justify-center shadow-sm relative">
        <LayoutTemplate className="w-10 h-10 text-muted-foreground" />
        <div className="absolute -bottom-2 -right-2 bg-primary w-8 h-8 rounded-full flex items-center justify-center border-2 border-background">
          <Search className="w-4 h-4 text-primary-foreground" />
        </div>
      </div>
      <h2 className="text-2xl font-bold mb-3 tracking-tight">Investigation Workspace</h2>
      <p className="text-sm mb-8 max-w-lg text-center text-muted-foreground leading-relaxed">
        The workspace is a secure, isolated environment containing logs, evidence files, and objectives for active cyber scenarios. You haven't selected a scenario to investigate. 
      </p>
      <Link 
        to={ROUTES.SCENARIOS}
        className="px-6 py-2.5 bg-primary hover:bg-primary/90 text-primary-foreground rounded-md transition-colors text-sm font-medium shadow-sm inline-flex items-center gap-2"
      >
        <Search className="w-4 h-4" />
        Browse Scenario Catalog
      </Link>
    </div>
  )
}
