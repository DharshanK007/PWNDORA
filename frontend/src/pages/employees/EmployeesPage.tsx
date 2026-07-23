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

import { ExportDirectoryDialog } from '@/components/common/dialog/ExportDirectoryDialog'
import { EmployeeDetailsDialog } from '@/components/common/dialog/EmployeeDetailsDialog'
import { useState } from 'react'
import { useLabSession } from '@/contexts/LabSessionContext'

export function EmployeesPage() {
  const { data, isLoading, isError, refetch } = useEmployees()
  const { currentStage, scenario } = useLabSession()
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null)
  const [isExportDialogOpen, setIsExportDialogOpen] = useState(false)

  // Only reveal the Export feature during Stage 4 of Silent Exfiltration
  const showExport = scenario?.id === 'silent_exfiltration' && currentStage === 4

  return (
    <div className="flex-1 space-y-6 pb-12">
      <PageHeader 
        title="Employees" 
        description="Manage enterprise personnel and access credentials."
        actions={
          showExport && (
            <button 
              onClick={() => setIsExportDialogOpen(true)}
              className="rounded-md bg-secondary px-4 py-2 text-sm font-medium text-secondary-foreground hover:bg-secondary/80 transition-colors flex items-center gap-2 animate-in fade-in slide-in-from-right-4 duration-500"
            >
              Export Directory
            </button>
          )
        }
      />

      <div className="w-full">
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
              onRowClick={(item) => setSelectedEmployee(item)}
            />
          </InfoPanel>
        )}
      </div>

      <EmployeeDetailsDialog
        employee={selectedEmployee}
        onClose={() => setSelectedEmployee(null)}
      />

      <ExportDirectoryDialog 
        isOpen={isExportDialogOpen} 
        onClose={() => setIsExportDialogOpen(false)} 
      />
    </div>
  )
}
