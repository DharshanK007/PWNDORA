import { useEffect, useRef } from 'react'
import { X, AlertTriangle, AlertCircle, Info } from 'lucide-react'
import { cn } from '@/lib/utils'

export type ConfirmationIntent = 'danger' | 'warning' | 'info'

interface ConfirmationDialogProps {
  isOpen: boolean
  title: string
  description: string
  confirmText?: string
  cancelText?: string
  intent?: ConfirmationIntent
  onConfirm: () => void
  onCancel: () => void
}

const intentStyles = {
  danger: {
    icon: AlertCircle,
    iconClass: 'text-destructive',
    bgClass: 'bg-destructive/10',
    btnClass: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
  },
  warning: {
    icon: AlertTriangle,
    iconClass: 'text-warning',
    bgClass: 'bg-warning/10',
    btnClass: 'bg-warning text-warning-foreground hover:bg-warning/90',
  },
  info: {
    icon: Info,
    iconClass: 'text-primary',
    bgClass: 'bg-primary/10',
    btnClass: 'bg-primary text-primary-foreground hover:bg-primary/90',
  },
}

export function ConfirmationDialog({
  isOpen,
  title,
  description,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  intent = 'info',
  onConfirm,
  onCancel,
}: ConfirmationDialogProps) {
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

  // Handle ESC key
  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    const handleCancel = (e: Event) => {
      e.preventDefault() // prevent native close to handle it reactively
      onCancel()
    }

    dialog.addEventListener('cancel', handleCancel)
    return () => dialog.removeEventListener('cancel', handleCancel)
  }, [onCancel])

  if (!isOpen) return null

  const { icon: Icon, iconClass, bgClass, btnClass } = intentStyles[intent]

  return (
    <dialog
      ref={dialogRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-transparent p-4 animate-in fade-in duration-200 backdrop:bg-background/80 backdrop:backdrop-blur-sm m-0 w-screen h-screen"
    >
      <div 
        className="w-full max-w-md rounded-xl border border-border bg-card p-6 shadow-xl relative animate-in zoom-in-95"
        role="document"
      >
        <button
          onClick={onCancel}
          className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground"
        >
          <X className="h-4 w-4" />
          <span className="sr-only">Close</span>
        </button>

        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-4">
            <div className={cn('flex h-10 w-10 items-center justify-center rounded-full', bgClass)}>
              <Icon className={cn('h-5 w-5', iconClass)} />
            </div>
            <div>
              <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
            </div>
          </div>
          
          <div className="pl-14">
            <p className="text-sm text-muted-foreground">{description}</p>
          </div>
        </div>

        <div className="mt-8 flex justify-end gap-3">
          <button
            autoFocus
            onClick={onCancel}
            className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className={cn(
              'inline-flex h-10 items-center justify-center rounded-md px-4 py-2 text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
              btnClass
            )}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </dialog>
  )
}
