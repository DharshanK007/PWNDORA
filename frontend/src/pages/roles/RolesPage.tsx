import { ShieldCheck } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { EntityCard } from '@/components/common/EntityCard'
import { useRoles } from '@/hooks/api/useRoles'
import { EmptyModule } from '@/components/common/EmptyModule'

export function RolesPage() {
  const { data: roles, isLoading, isError, refetch } = useRoles()

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Role-Based Access Control" 
        description="Define custom roles and manage granular permissions across the enterprise."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Roles"
          description="There was an error communicating with the backend API."
          icon={ShieldCheck}
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
        <div className="grid gap-4 md:grid-cols-2 animate-pulse">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-40 rounded-xl bg-card border border-border" />
          ))}
        </div>
      ) : roles?.length === 0 ? (
        <EmptyModule title="No Roles Defined" icon={ShieldCheck} />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {roles?.map(role => (
            <EntityCard
              key={role.id}
              title={role.name}
              icon={<ShieldCheck className="h-5 w-5" />}
              footer={
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Active Members:</span>
                  <span className="font-semibold text-foreground">{role.member_count}</span>
                </div>
              }
            >
              <div className="flex flex-col gap-2">
                <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
                  Permissions ({role.permissions.length})
                </span>
                <div className="flex flex-wrap gap-2">
                  {role.permissions.map(p => (
                    <span key={p} className="rounded border border-border bg-background px-2 py-0.5 text-xs text-muted-foreground">
                      {p}
                    </span>
                  ))}
                </div>
              </div>
            </EntityCard>
          ))}
        </div>
      )}
    </div>
  )
}
