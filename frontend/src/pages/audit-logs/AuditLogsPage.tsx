import { ClipboardList } from 'lucide-react'
import { PlaceholderPage } from '@/components/common/PlaceholderPage'

export default function AuditLogsPage() {
  return (
    <PlaceholderPage 
      title="Audit Logs" 
      description="Immutable record of all enterprise activities, user logins, and configuration changes."
      icon={ClipboardList} 
    />
  )
}
