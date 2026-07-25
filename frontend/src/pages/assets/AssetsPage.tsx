import { Server, Search } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { DataTable, type Column } from '@/components/table/DataTable'
import { StatusBadge, type StatusVariant } from '@/components/common/StatusBadge'
import { useAssets } from '@/hooks/api/useAssets'
import type { Asset } from '@/services/assets'
import { EmptyModule } from '@/components/common/EmptyModule'
import { InfoPanel } from '@/components/common/InfoPanel'
import { AssetDetailsDialog } from '@/components/common/dialog/AssetDetailsDialog'
import { useState, useMemo } from 'react'

const columns: Column<Asset>[] = [
  { key: 'name', header: 'Asset Name', className: 'font-medium', sortable: true },
  { key: 'ip_address', header: 'IP Address' },
  {
    key: 'status',
    header: 'Status',
    sortable: true,
    cell: (item) => {
      let variant: StatusVariant = 'default'
      if (item.status === 'ONLINE') variant = 'active'
      if (item.status === 'OFFLINE') variant = 'inactive'
      if (item.status === 'MAINTENANCE') variant = 'warning'
      if (item.status === 'COMPROMISED') variant = 'critical'
      
      return <StatusBadge status={item.status} variant={variant} />
    }
  },
  { key: 'asset_group', header: 'Group' },
  { key: 'last_patch_date', header: 'Patch Date', sortable: true, cell: (item) => item.last_patch_date || 'N/A' }
]

export function AssetsPage() {
  const { data, isLoading, isError, refetch } = useAssets(0, 1000)
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null)
  
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('ALL')
  const [groupFilter, setGroupFilter] = useState('ALL')
  
  const [tempSearchQuery, setTempSearchQuery] = useState('')
  const [tempStatusFilter, setTempStatusFilter] = useState('ALL')
  const [tempGroupFilter, setTempGroupFilter] = useState('ALL')
  
  const [sortConfig, setSortConfig] = useState<{key: string, direction: 'asc'|'desc'} | null>(null)

  const filteredAndSortedData = useMemo(() => {
    if (!data?.items) return []
    
    let result = [...data.items]
    
    // Filter by search query
    if (searchQuery) {
      const q = searchQuery.trim().toLowerCase()
      result = result.filter(asset => 
        (asset.name && asset.name.toLowerCase().includes(q)) ||
        (asset.ip_address && asset.ip_address.toLowerCase().includes(q)) ||
        (asset.status && asset.status.toLowerCase().includes(q))
      )
    }
    
    // Filter by status dropdown
    if (statusFilter !== 'ALL') {
      result = result.filter(asset => asset.status?.toUpperCase() === statusFilter.toUpperCase())
    }
    
    // Filter by group dropdown
    if (groupFilter !== 'ALL') {
      result = result.filter(asset => asset.asset_group === groupFilter)
    }
    
    // Sort
    if (sortConfig) {
      result.sort((a, b) => {
        let aVal = (a as any)[sortConfig.key] || ''
        let bVal = (b as any)[sortConfig.key] || ''
        
        if (sortConfig.key === 'last_patch_date') {
          // Empty patch dates should go to bottom
          if (!aVal) aVal = '9999-12-31'
          if (!bVal) bVal = '9999-12-31'
        }
        
        if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1
        if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1
        return 0
      })
    }
    
    return result
  }, [data?.items, searchQuery, statusFilter, groupFilter, sortConfig])

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
        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-4">
            <div className="relative flex-1 min-w-[250px] max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input 
                type="text" 
                placeholder="Search assets by name, IP, or status..." 
                className="w-full pl-9 pr-4 py-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            
            <select 
              value={tempStatusFilter}
              onChange={(e) => setTempStatusFilter(e.target.value)}
              className="px-3 py-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="ALL">All Statuses</option>
              <option value="ONLINE">Online</option>
              <option value="OFFLINE">Offline</option>
              <option value="MAINTENANCE">Maintenance</option>
              <option value="COMPROMISED">Compromised</option>
              <option value="NEW">New</option>
              <option value="REGISTERED">Registered</option>
            </select>
            
            <select 
              value={tempGroupFilter}
              onChange={(e) => setTempGroupFilter(e.target.value)}
              className="px-3 py-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="ALL">All Groups</option>
              <option value="Production">Production</option>
              <option value="Network">Network</option>
              <option value="HVAC">HVAC</option>
              <option value="Safety">Safety</option>
              <option value="Control Systems">Control Systems</option>
            </select>
            
            <button 
              onClick={() => {
                setStatusFilter(tempStatusFilter)
                setGroupFilter(tempGroupFilter)
              }}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              Apply Filter
            </button>
            
            <div className="text-sm text-muted-foreground ml-auto">
              Showing {filteredAndSortedData.length} assets
            </div>
          </div>
          
          <InfoPanel title="Device Inventory">
            <DataTable
              data={filteredAndSortedData}
              columns={columns}
              isLoading={isLoading}
              keyExtractor={(item) => item.id}
              emptyMessage="No industrial assets match your search."
              onRowClick={(item) => setSelectedAsset(item)}
              onSort={(key, direction) => setSortConfig({key, direction})}
            />
          </InfoPanel>
        </div>
      )}

      <AssetDetailsDialog
        asset={selectedAsset}
        onClose={() => setSelectedAsset(null)}
      />
    </div>
  )
}
