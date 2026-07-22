import { useEffect, useRef, useState } from 'react'
import { X, Server, Cpu, AlertTriangle, Zap, CheckCircle2 } from 'lucide-react'
import api from '@/lib/axios'
import { useLabSession } from '@/contexts/LabSessionContext'

interface AssetDetailsDialogProps {
  asset: any | null
  onClose: () => void
}

export function AssetDetailsDialog({ asset, onClose }: AssetDetailsDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const [details, setDetails] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isPushing, setIsPushing] = useState(false)
  const [pushResult, setPushResult] = useState<string | null>(null)
  const { refetch } = useLabSession()

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    if (asset) {
      dialog.showModal()
      setDetails(asset)
      setPushResult(null)
      setIsLoading(true)
      api.get('/devices/' + asset.id)
        .then(({ data }) => setDetails(data))
        .catch((err) => console.error('Failed to fetch asset details:', err))
        .finally(() => setIsLoading(false))
    } else {
      dialog.close()
      setDetails(null)
      setPushResult(null)
    }
  }, [asset])

  const handleFirmwarePush = async () => {
    if (!details) return
    setIsPushing(true)
    setPushResult(null)
    try {
      // Exploit Client Trust / Session Flaw by sending X-User-Role: Administrator header
      const res = await api.post(
        '/devices/' + details.id + '/firmware-push',
        {},
        { headers: { 'X-User-Role': 'Administrator' } }
      )
      setPushResult(res.data?.message || 'Firmware push executed successfully via privilege escalation!')
      // Refresh global lab session state
      if (refetch) await refetch()
    } catch (err: any) {
      console.error('Firmware push failed:', err)
      setPushResult(err.response?.data?.detail || 'Failed to push firmware. Ensure Stage 4 is active.')
    } finally {
      setIsPushing(false)
    }
  }

  if (!asset) return null

  return (
    <dialog
      ref={dialogRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-transparent p-4 animate-in fade-in duration-200 backdrop:bg-background/80 backdrop:backdrop-blur-sm m-0 w-screen h-screen"
    >
      <div className="flex flex-col w-full max-w-xl rounded-xl border border-border bg-card shadow-2xl relative animate-in zoom-in-95 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border p-4 bg-muted/40">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
              <Server className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h2 className="text-lg font-semibold tracking-tight">{details?.name || 'Asset Details'}</h2>
              <span className="text-xs text-muted-foreground font-mono">{details?.ip_address || 'Loading...'}</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 text-sm bg-background">
          {isLoading ? (
            <div className="p-8 text-center text-muted-foreground">Loading asset configuration...</div>
          ) : details ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4 p-4 rounded-lg bg-muted/30 border border-border/50 text-xs">
                <div>
                  <span className="text-muted-foreground block font-medium">Status</span>
                  <span className="font-semibold text-foreground uppercase">{details.status || 'N/A'}</span>
                </div>
                <div>
                  <span className="text-muted-foreground block font-medium">IP Address</span>
                  <span className="font-mono text-foreground">{details.ip_address || 'N/A'}</span>
                </div>
                <div>
                  <span className="text-muted-foreground block font-medium">MAC Address</span>
                  <span className="font-mono text-foreground">{details.mac_address || 'N/A'}</span>
                </div>
                <div>
                  <span className="text-muted-foreground block font-medium">Asset Group</span>
                  <span className="text-foreground">{details.asset_group || 'Production'}</span>
                </div>
              </div>

              {/* Special highlight & Firmware Push Action for PLC Line 2 */}
              {details.name === 'PLC-Line2-FW-Controller' && (
                <div className="p-4 rounded-lg border border-amber-500/40 bg-amber-500/10 space-y-3">
                  <div className="flex items-center gap-2 text-amber-500 font-semibold text-xs">
                    <AlertTriangle className="h-4 w-4 shrink-0" />
                    <span>OUTDATED FIRMWARE WARNING</span>
                  </div>
                  <div className="text-xs space-y-1 font-mono text-muted-foreground">
                    <p><strong>Operating System:</strong> OT-RTOS v1.2.3 (Outdated)</p>
                    <p><strong>Vendor:</strong> Vendor PLC Corp</p>
                    <p><strong>Maintenance Advisory:</strong> Deferred update — vendor advisory pending review</p>
                    <p className="pt-1 text-primary font-semibold">
                      <strong>Assigned Lead Engineer:</strong> Marcus Chen (OT Operations)
                    </p>
                  </div>

                  {/* Push Firmware Action Button */}
                  <div className="pt-2 border-t border-amber-500/30 space-y-2">
                    <button
                      onClick={handleFirmwarePush}
                      disabled={isPushing}
                      className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-white font-medium text-xs transition-all shadow-md active:scale-98 disabled:opacity-50"
                    >
                      <Zap className="h-4 w-4" />
                      <span>
                        {isPushing
                          ? 'Pushing Firmware (Overriding X-User-Role)...'
                          : 'Push Firmware Update (Elevate Role: Administrator)'}
                      </span>
                    </button>

                    {pushResult && (
                      <div className="p-2.5 rounded-md bg-emerald-500/15 border border-emerald-500/40 text-emerald-400 text-xs flex items-center gap-2 font-mono">
                        <CheckCircle2 className="h-4 w-4 shrink-0" />
                        <span>{pushResult}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div className="space-y-2 text-xs">
                <div className="flex items-center gap-2 text-muted-foreground font-semibold">
                  <Cpu className="h-4 w-4 text-primary" />
                  <span>Device Properties</span>
                </div>
                <div className="p-3 rounded-lg border border-border/60 bg-card space-y-1.5 font-mono text-xs">
                  <p><span className="text-muted-foreground">Location ID:</span> {details.location_id || 'Factory Site A'}</p>
                  <p><span className="text-muted-foreground">Firmware ID:</span> {details.firmware_id || 'v1.2.3'}</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-4 text-center text-muted-foreground">No details available.</div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-border p-4 bg-muted/40 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80 text-xs font-medium"
          >
            Close Details
          </button>
        </div>
      </div>
    </dialog>
  )
}
