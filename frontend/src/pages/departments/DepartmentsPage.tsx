import { Building2 } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { EntityCard } from '@/components/common/EntityCard'
import { useDepartments } from '@/hooks/api/useDepartments'
import { EmptyModule } from '@/components/common/EmptyModule'

export function DepartmentsPage() {
  const { data, isLoading, isError, refetch } = useDepartments()

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Departments" 
        description="Enterprise organizational structure."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Departments"
          description="There was an error communicating with the backend API."
          icon={Building2}
          action={
            <button 
              onClick={() => refetch()} 
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              Try Again
            </button>
          }
        />
      ) : isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 animate-pulse">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-32 rounded-xl bg-card border border-border" />
          ))}
        </div>
      ) : data?.items.length === 0 ? (
        <EmptyModule title="No Departments" icon={Building2} />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {data?.items.map(dept => (
            <EntityCard
              key={dept.id}
              title={dept.name}
              subtitle={dept.description || 'No description provided'}
              icon={<Building2 className="h-5 w-5" />}
              footer={
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Manager ID: {dept.manager_id || 'None'}</span>
                  <span>{dept.location || 'HQ'}</span>
                </div>
              }
            />
          ))}
        </div>
      )}
    </div>
  )
}
