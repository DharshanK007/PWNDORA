import { useEffect, useRef } from 'react'
import { X, FileText } from 'lucide-react'

interface ReportViewerDialogProps {
  isOpen: boolean
  title: string
  content: string
  onClose: () => void
}

export function ReportViewerDialog({
  isOpen,
  title,
  content,
  onClose,
}: ReportViewerDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    if (isOpen) {
      dialog.showModal()
    } else {
      dialog.close()
    }
  }, [isOpen])

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    const handleCancel = (e: Event) => {
      e.preventDefault()
      onClose()
    }

    dialog.addEventListener('cancel', handleCancel)
    return () => dialog.removeEventListener('cancel', handleCancel)
  }, [onClose])

  if (!isOpen) return null

  return (
    <dialog
      ref={dialogRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-transparent p-4 animate-in fade-in duration-200 backdrop:bg-background/80 backdrop:backdrop-blur-sm m-0 w-screen h-screen"
    >
      <div 
        className="flex flex-col w-full max-w-4xl max-h-[85vh] rounded-xl border border-border bg-card shadow-xl relative animate-in zoom-in-95 overflow-hidden"
        role="document"
      >
        <div className="flex items-center justify-between border-b border-border p-4 bg-muted/30">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
              <FileText className="h-5 w-5 text-primary" />
            </div>
            <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
          </div>
          <button
            onClick={onClose}
            className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          >
            <X className="h-5 w-5" />
            <span className="sr-only">Close</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 bg-background">
          <pre className="whitespace-pre-wrap font-sans text-sm text-foreground/90 leading-relaxed">
            {content}
          </pre>
        </div>

        <div className="border-t border-border p-4 bg-muted/30 flex justify-end">
          <button
            onClick={onClose}
            className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            Close Report
          </button>
        </div>
      </div>
    </dialog>
  )
}
