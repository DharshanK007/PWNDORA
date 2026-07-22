import { Server } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { DataTable, type Column } from '@/components/table/DataTable'
import { StatusBadge, type StatusVariant } from '@/components/common/StatusBadge'
import { useAssets } from '@/hooks/api/useAssets'
import type { Asset } from '@/services/assets'
import { EmptyModule } from '@/components/common/EmptyModule'
import { InfoPanel } from '@/components/common/InfoPanel'

const columns: Column<Asset>[] = [
  { key: 'name', header: 'Asset Name', className: 'font-medium' },
  { key: 'type', header: 'Type' },
  { key: 'ip_address', header: 'IP Address' },
  {
    key: 'status',
    header: 'Status',
    cell: (item) => {
      let variant: StatusVariant = 'default'
      if (item.status === 'ONLINE') variant = 'active'
      if (item.status === 'OFFLINE') variant = 'inactive'
      if (item.status === 'MAINTENANCE') variant = 'warning'
      if (item.status === 'COMPROMISED') variant = 'critical'
      
      return <StatusBadge status={item.status} variant={variant} />
    }
  },
  { key: 'location', header: 'Location' },
  { key: 'firmware_version', header: 'Firmware' }
]

import { AssetDetailsDialog } from '@/components/common/dialog/AssetDetailsDialog'
import { useState } from 'react'

export function AssetsPage() {
  const { data, isLoading, isError, refetch } = useAssets()
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null)

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Industrial Assets" 
        description="Inventory of all PLCs, HMIs, Servers, and Edge Devices."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Assets"
          description="There was an error communicating with the backend API."
          icon={Server}
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
        <InfoPanel title="Device Inventory">
          <DataTable
            data={data?.items || []}
            columns={columns}
            isLoading={isLoading}
            keyExtractor={(item) => item.id}
            emptyMessage="No industrial assets found."
            onRowClick={(item) => setSelectedAsset(item)}
          />
        </InfoPanel>
      )}

      <AssetDetailsDialog
        asset={selectedAsset}
        onClose={() => setSelectedAsset(null)}
      />
    </div>
  )
}
