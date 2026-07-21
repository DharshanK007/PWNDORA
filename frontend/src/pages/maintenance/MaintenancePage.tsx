import { Wrench } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { DataTable, type Column } from '@/components/table/DataTable'
import { StatusBadge, type StatusVariant } from '@/components/common/StatusBadge'
import { useTickets } from '@/hooks/api/useMaintenance'
import type { MaintenanceTicket } from '@/services/maintenance'
import { EmptyModule } from '@/components/common/EmptyModule'
import { InfoPanel } from '@/components/common/InfoPanel'

const columns: Column<MaintenanceTicket>[] = [
  { key: 'title', header: 'Ticket Title', className: 'font-medium' },
  { key: 'device_id', header: 'Device ID' },
  {
    key: 'priority',
    header: 'Priority',
    cell: (item) => {
      let variant: StatusVariant = 'default'
      if (item.priority === 'HIGH' || item.priority === 'CRITICAL') variant = 'critical'
      if (item.priority === 'MEDIUM') variant = 'warning'
      
      return <StatusBadge status={item.priority} variant={variant} />
    }
  },
  {
    key: 'status',
    header: 'Status',
    cell: (item) => {
      let variant: StatusVariant = 'default'
      if (item.status === 'OPEN') variant = 'active'
      if (item.status === 'IN_PROGRESS') variant = 'warning'
      if (item.status === 'RESOLVED' || item.status === 'CLOSED') variant = 'inactive'
      
      return <StatusBadge status={item.status} variant={variant} />
    }
  },
  { key: 'assigned_to', header: 'Assigned Engineer' },
  { 
    key: 'updated_at', 
    header: 'Last Updated',
    cell: (item) => new Date(item.updated_at).toLocaleDateString()
  }
]

export function MaintenancePage() {
  const { data, isLoading, isError, refetch } = useTickets()

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Maintenance Operations" 
        description="Track and manage enterprise hardware repairs, firmware updates, and scheduled maintenance."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Tickets"
          description="There was an error communicating with the backend API."
          icon={Wrench}
          action={
            <button 
              onClick={() => refetch()} 
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              Try Again
            </button>
          }
        />
      ) : (
        <InfoPanel title="Active Tickets">
          <DataTable
            data={data?.items || []}
            columns={columns}
            isLoading={isLoading}
            keyExtractor={(item) => item.id}
            emptyMessage="No open maintenance tasks."
          />
        </InfoPanel>
      )}
    </div>
  )
}
