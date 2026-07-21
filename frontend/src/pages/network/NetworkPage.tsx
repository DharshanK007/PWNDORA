import { Network as NetworkIcon, ServerCrash } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { EntityCard } from '@/components/common/EntityCard'
import { StatusBadge, type StatusVariant } from '@/components/common/StatusBadge'
import { useAssets } from '@/hooks/api/useAssets'
import { EmptyModule } from '@/components/common/EmptyModule'

export function NetworkPage() {
  const { data, isLoading, isError, refetch } = useAssets()

  const networkDevices = data?.items.filter(
    d => d.asset_group?.toLowerCase() === 'network'
  ) || []

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Network Topology" 
        description="Enterprise network layout, zones, and connectivity status."
      />

      {isError ? (
        <EmptyModule
          title="Failed to Load Network Devices"
          description="There was an error communicating with the backend API."
          icon={ServerCrash}
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
            <div key={i} className="h-40 rounded-xl bg-card border border-border" />
          ))}
        </div>
      ) : networkDevices.length === 0 ? (
        <EmptyModule 
          title="No Network Devices" 
          description="No switches, routers, or firewalls are currently registered in the topology." 
          icon={NetworkIcon} 
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {networkDevices.map(device => {
            let variant: StatusVariant = 'default'
            if (device.status === 'ONLINE') variant = 'active'
            if (device.status === 'OFFLINE') variant = 'inactive'
            if (device.status === 'COMPROMISED') variant = 'critical'

            return (
              <EntityCard
                key={device.id}
                title={device.name}
                subtitle={`IP: ${device.ip_address || 'N/A'}`}
                icon={<NetworkIcon className="h-5 w-5" />}
                badges={<StatusBadge status={device.status} variant={variant} />}
                footer={
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">{device.asset_group}</span>
                    <span className="text-muted-foreground">{device.mac_address || 'N/A'}</span>
                  </div>
                }
              >
                <div className="flex flex-col gap-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Zone</span>
                    <span className="font-medium text-foreground">{device.location || 'Default Zone'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Firmware</span>
                    <span className="font-medium text-foreground">{device.firmware_version || 'Unknown'}</span>
                  </div>
                </div>
              </EntityCard>
            )
          })}
        </div>
      )}
    </div>
  )
}
