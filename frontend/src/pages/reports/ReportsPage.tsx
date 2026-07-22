import { ClipboardList } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { DataTable, type Column } from '@/components/table/DataTable'
import { StatusBadge, type StatusVariant } from '@/components/common/StatusBadge'
import { useReports } from '@/hooks/api/useReports'
import type { Report } from '@/services/reports'
import { EmptyModule } from '@/components/common/EmptyModule'
import { InfoPanel } from '@/components/common/InfoPanel'
import { ReportViewerDialog } from '@/components/common/dialog/ReportViewerDialog'
import { useState } from 'react'

const columns: Column<Report>[] = [
  { key: 'title', header: 'Report Name', className: 'font-medium' },
  { key: 'type', header: 'Category' },
  {
    key: 'status',
    header: 'Status',
    cell: (item) => {
      let variant: StatusVariant = 'default'
      if (item.status === 'PUBLISHED') variant = 'active'
      if (item.status === 'DRAFT') variant = 'warning'
      if (item.status === 'ARCHIVED') variant = 'inactive'
      
      return <StatusBadge status={item.status} variant={variant} />
    }
  },
  { key: 'generated_by', header: 'Author' },
  { 
    key: 'created_at', 
    header: 'Date Generated',
    cell: (item) => new Date(item.created_at).toLocaleDateString()
  }
]

export function ReportsPage() {
  const { data, isLoading, isError, refetch } = useReports()
  const [selectedReport, setSelectedReport] = useState<Report | null>(null)

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Analytics & Reports" 
        description="Access and generate enterprise intelligence, compliance, and security reports."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Reports"
          description="There was an error communicating with the backend API."
          icon={ClipboardList}
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
        <InfoPanel title="Available Documents">
          <DataTable
            data={data?.items || []}
            columns={columns}
            isLoading={isLoading}
            keyExtractor={(item) => item.id}
            emptyMessage="No reports have been generated yet."
            onRowClick={(item) => setSelectedReport(item)}
          />
        </InfoPanel>
      )}

      {selectedReport && (
        <ReportViewerDialog
          isOpen={!!selectedReport}
          title={selectedReport.title}
          content={selectedReport.summary || 'No content available for this report.'}
          onClose={() => setSelectedReport(null)}
        />
      )}
    </div>
  )
}
