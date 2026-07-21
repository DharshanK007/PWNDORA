import { UserCog } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { DataTable, type Column } from '@/components/table/DataTable'
import { StatusBadge, type StatusVariant } from '@/components/common/StatusBadge'
import { useUsers } from '@/hooks/api/useUsers'
import type { User } from '@/services/users'
import { EmptyModule } from '@/components/common/EmptyModule'
import { InfoPanel } from '@/components/common/InfoPanel'

const columns: Column<User>[] = [
  { key: 'email', header: 'Email Address', className: 'font-medium' },
  { key: 'role', header: 'Role' },
  {
    key: 'is_active',
    header: 'Status',
    cell: (item) => {
      const status = item.is_active ? 'ACTIVE' : 'DISABLED'
      const variant: StatusVariant = item.is_active ? 'active' : 'inactive'
      return <StatusBadge status={status} variant={variant} />
    }
  },
  {
    key: 'is_superuser',
    header: 'Privileges',
    cell: (item) => (
      item.is_superuser ? <span className="text-xs font-semibold text-amber-500">Superuser</span> : <span className="text-muted-foreground">-</span>
    )
  },
  { 
    key: 'created_at', 
    header: 'Joined Date',
    cell: (item) => new Date(item.created_at).toLocaleDateString()
  }
]

export function UsersPage() {
  const { data, isLoading, isError, refetch } = useUsers()

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="User Management" 
        description="Manage enterprise application users, system privileges, and account status."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Users"
          description="There was an error communicating with the backend API."
          icon={UserCog}
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
        <InfoPanel title="Registered Accounts">
          <DataTable
            data={data?.items || []}
            columns={columns}
            isLoading={isLoading}
            keyExtractor={(item) => item.id}
            emptyMessage="No users registered in the system."
          />
        </InfoPanel>
      )}
    </div>
  )
}
