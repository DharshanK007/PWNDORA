import { useEffect, useRef, useState } from 'react'
import { X, UserCheck, FileText } from 'lucide-react'
import api from '@/lib/axios'

interface EmployeeDetailsDialogProps {
  employee: any | null
  onClose: () => void
}

export function EmployeeDetailsDialog({ employee, onClose }: EmployeeDetailsDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const [details, setDetails] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    if (employee) {
      dialog.showModal()
      setDetails(employee)
      setIsLoading(true)
      api.get('/employees/' + employee.id)
        .then(({ data }) => setDetails(data))
        .catch((err) => console.error('Failed to fetch employee details:', err))
        .finally(() => setIsLoading(false))
    } else {
      dialog.close()
      setDetails(null)
    }
  }, [employee])

  if (!employee) return null

  return (
    <dialog
      ref={dialogRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-transparent p-4 animate-in fade-in duration-200 backdrop:bg-background/80 backdrop:backdrop-blur-sm m-0 w-screen h-screen"
    >
      <div className="flex flex-col w-full max-w-xl rounded-xl border border-border bg-card shadow-2xl relative animate-in zoom-in-95 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border p-4 bg-muted/40">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 font-semibold text-primary">
              {details ? details.first_name[0] + details.last_name[0] : <UserCheck className="h-5 w-5" />}
            </div>
            <div>
              <h2 className="text-lg font-semibold tracking-tight">{details ? details.first_name + ' ' + details.last_name : 'Employee Profile'}</h2>
              <span className="text-xs text-muted-foreground font-mono">{details?.title || 'Loading...'}</span>
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
            <div className="p-8 text-center text-muted-foreground">Retrieving employee record...</div>
          ) : details ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4 p-4 rounded-lg bg-muted/30 border border-border/50 text-xs">
                <div>
                  <span className="text-muted-foreground block font-medium">Full Name</span>
                  <span className="font-semibold text-foreground">{details.first_name} {details.last_name}</span>
                </div>
                <div>
                  <span className="text-muted-foreground block font-medium">Job Title</span>
                  <span className="text-foreground">{details.title || 'N/A'}</span>
                </div>
                <div>
                  <span className="text-muted-foreground block font-medium">Phone</span>
                  <span className="font-mono text-foreground">{details.phone || 'N/A'}</span>
                </div>
                <div>
                  <span className="text-muted-foreground block font-medium">Clearance Level</span>
                  <span className="font-semibold text-primary">{details.clearance_level || 'Level 4 (OT)'}</span>
                </div>
              </div>

              {/* Special Note Leak for Marcus Chen */}
              {(details.first_name === 'Marcus' || details.last_name === 'Chen') && (
                <div className="p-4 rounded-lg border border-primary/40 bg-primary/10 space-y-2">
                  <div className="flex items-center gap-2 text-primary font-semibold text-xs">
                    <FileText className="h-4 w-4 shrink-0" />
                    <span>ENGINEER INTERNAL NOTE (LEAKED FINDING)</span>
                  </div>
                  <p className="text-xs font-mono text-foreground leading-relaxed">
                    "Line 2 halt issue was logged under ticket #402. Check deployment audit logs via the top <strong>Search bar</strong> using the term <code>firmware</code> or injection patterns to retrieve raw deployment events."
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="p-4 text-center text-muted-foreground">No employee data found.</div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-border p-4 bg-muted/40 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80 text-xs font-medium"
          >
            Close Profile
          </button>
        </div>
      </div>
    </dialog>
  )
}
