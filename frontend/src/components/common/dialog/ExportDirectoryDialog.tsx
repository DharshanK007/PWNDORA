import { useEffect, useRef, useState } from 'react'
import { X, Download, ShieldAlert } from 'lucide-react'
import api from '@/lib/axios'

interface ExportDirectoryDialogProps {
  isOpen: boolean
  onClose: () => void
}

export function ExportDirectoryDialog({ isOpen, onClose }: ExportDirectoryDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  
  const [exportKey, setExportKey] = useState("")
  const [exportResult, setExportResult] = useState<any>(null)
  const [exportError, setExportError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    if (isOpen) {
      dialog.showModal()
      setExportKey("")
      setExportResult(null)
      setExportError(null)
    } else {
      dialog.close()
    }
  }, [isOpen])

  const handleExport = async () => {
    setIsLoading(true)
    setExportError(null)
    setExportResult(null)
    try {
      const res = await api.get('/employees/export', {
        headers: exportKey ? { 'X-Service-Key': exportKey } : {}
      })
      setExportResult(res.data)
    } catch (err: any) {
      setExportError(err.response?.data?.detail || "Export failed. Admin access required.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <dialog
      ref={dialogRef}
      onCancel={onClose}
      className="fixed inset-0 z-50 flex items-center justify-center bg-transparent p-4 animate-in fade-in duration-200 backdrop:bg-background/80 backdrop:backdrop-blur-sm m-0 w-screen h-screen"
    >
      <div className="flex flex-col w-full max-w-lg rounded-xl border border-border bg-card shadow-2xl relative animate-in zoom-in-95 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border p-4 bg-muted/40">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 font-semibold text-primary">
              <Download className="h-5 w-5" />
            </div>
            <div>
              <h2 className="text-lg font-semibold tracking-tight">Export Employee Directory</h2>
              <span className="text-xs text-muted-foreground font-mono">Bulk Data Processing</span>
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
        <div className="p-6 overflow-y-auto max-h-[60vh] space-y-4">
          <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg space-y-2">
            <div className="flex items-center gap-2 text-amber-500">
              <ShieldAlert className="h-4 w-4" />
              <span className="font-semibold text-xs">ADMINISTRATOR PRIVILEGES REQUIRED</span>
            </div>
            <p className="text-xs text-amber-500/80">
              Exporting the full employee directory accesses sensitive PII. Standard users are restricted from this action. Internal services may override this via authorized service tokens.
            </p>
          </div>

          <div className="space-y-3 mt-4">
            <div>
              <label className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-1 block">
                Service Override Token (Optional)
              </label>
              <input 
                type="password" 
                value={exportKey}
                onChange={(e) => setExportKey(e.target.value)}
                placeholder="Paste service token here..."
                className="w-full text-sm px-3 py-2 bg-background border border-border rounded-md focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            
            <button 
              onClick={handleExport}
              disabled={isLoading}
              className="w-full py-2 bg-primary text-primary-foreground text-sm font-semibold rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              {isLoading ? "Exporting..." : "Run Export"}
            </button>

            {exportError && (
              <div className="mt-3 p-3 bg-destructive/10 border border-destructive/20 text-destructive text-sm rounded-md">
                {exportError}
              </div>
            )}

            {exportResult && (
              <div className="mt-3 p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-[10px] rounded-md overflow-x-auto max-h-48 overflow-y-auto">
                <div className="font-semibold mb-1">Export Successful ({exportResult.length} records):</div>
                <pre>{JSON.stringify(exportResult, null, 2)}</pre>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-border p-4 bg-muted/40 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80 text-xs font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </dialog>
  )
}
