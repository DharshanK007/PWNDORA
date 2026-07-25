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
  { 
    key: 'created_at', 
    header: 'Date Generated',
    cell: (item) => new Date(item.created_at.endsWith('Z') ? item.created_at : item.created_at + 'Z').toLocaleString()
  },
  {
    key: 'download',
    header: 'Download',
    cell: () => (
      <button className="px-3 py-1 bg-primary text-primary-foreground text-xs font-semibold rounded hover:bg-primary/90 transition-colors">
        View & Download
      </button>
    )
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
            data={data?.items ? [...data.items].sort((a,b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()).slice(0, 1) : []}
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
          reportId={selectedReport.id}
          title={selectedReport.title}
          content={selectedReport.summary || 'No content available for this report.'}
          status={selectedReport.status}
          onClose={() => setSelectedReport(null)}
          onSaved={() => {
            refetch()
          }}
        />
      )}
    </div>
  )
}
