import { PageHeader } from '@/components/common/PageHeader'
import { EmptyState } from '@/components/common/EmptyState'
import { Construction } from 'lucide-react'

export function InvestigationPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Investigation"
        description="Active investigation workspace and clue discovery"
      />
      <EmptyState
        icon={Construction}
        title="Coming in Step 2"
        description="This module will be connected to the backend in the next step."
      />
    </div>
  )
}
