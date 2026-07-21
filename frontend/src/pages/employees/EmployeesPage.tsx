import { Users } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { DataTable, type Column } from '@/components/table/DataTable'
import { StatusBadge, type StatusVariant } from '@/components/common/StatusBadge'
import { useEmployees } from '@/hooks/api/useEmployees'
import type { Employee } from '@/services/employees'
import { EmptyModule } from '@/components/common/EmptyModule'
import { InfoPanel } from '@/components/common/InfoPanel'

const columns: Column<Employee>[] = [
  {
    key: 'name',
    header: 'Name',
    cell: (item) => (
      <div className="flex items-center gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-xs font-medium text-primary">
          {item.first_name[0]}{item.last_name[0]}
        </div>
        <div className="flex flex-col">
          <span className="font-medium text-foreground">{item.first_name} {item.last_name}</span>
          <span className="text-xs text-muted-foreground">{item.phone || 'No phone'}</span>
        </div>
      </div>
    ),
  },
  { key: 'title', header: 'Role/Title' },
  { key: 'department_id', header: 'Department ID' },
  {
    key: 'status',
    header: 'Status',
    cell: (item) => {
      let variant: StatusVariant = 'default'
      if (item.status === 'ACTIVE') variant = 'active'
      if (item.status === 'INACTIVE') variant = 'inactive'
      if (item.status === 'ON_LEAVE') variant = 'warning'
      
      return <StatusBadge status={item.status} variant={variant} />
    }
  },
  { key: 'clearance_level', header: 'Clearance' }
]

export function EmployeesPage() {
  const { data, isLoading, isError, refetch } = useEmployees()

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Employees" 
        description="Manage enterprise personnel and access credentials."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Employees"
          description="There was an error communicating with the backend API."
          icon={Users}
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
        <InfoPanel title="Personnel Directory">
          <DataTable
            data={data?.items || []}
            columns={columns}
            isLoading={isLoading}
            keyExtractor={(item) => item.id}
            emptyMessage="No employees found in the organization."
          />
        </InfoPanel>
      )}
    </div>
  )
}
