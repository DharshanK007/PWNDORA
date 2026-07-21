import { Activity } from 'lucide-react'
import { PlaceholderPage } from '@/components/common/PlaceholderPage'

export default function MonitoringPage() {
  return (
    <PlaceholderPage 
      title="System Monitoring" 
      description="Real-time monitoring of all industrial assets, PLCs, and network traffic."
      icon={Activity} 
    />
  )
}
