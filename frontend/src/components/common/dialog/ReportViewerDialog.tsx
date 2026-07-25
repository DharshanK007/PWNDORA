import { useEffect, useRef, useState } from 'react'
import { X, FileText, Loader2 } from 'lucide-react'
import { ReportInfographics, InfographicData } from './ReportInfographics'

// We conditionally import html2pdf so it doesn't break SSR (if applicable) or load immediately
let html2pdf: any = null
import('html2pdf.js').then((module) => {
  html2pdf = module.default
})

interface ReportViewerDialogProps {
  isOpen: boolean
  reportId?: string
  title: string
  content: string
  status?: string
  onClose: () => void
  onSaved?: () => void
}

export function ReportViewerDialog({
  isOpen,
  reportId,
  title,
  content,
  status = 'Draft',
  onClose,
  onSaved,
}: ReportViewerDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false)
  const isSubmitted = status === 'Under Review' || status === 'Approved' || status === 'Published'

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
    const handleCancel = (e: Event) => {
      e.preventDefault()
      onClose()
    }
    const dialog = dialogRef.current
    if (dialog) {
      dialog.addEventListener('cancel', handleCancel)
      return () => dialog.removeEventListener('cancel', handleCancel)
    }
  }, [onClose])

  if (!isOpen) return null

  // Extract Infographics Data if present
  let cleanContent = content
  let infographicsData: InfographicData[] = []
  
  if (content.includes('<!-- [INFOGRAPHICS_DATA]')) {
    const parts = content.split('<!-- [INFOGRAPHICS_DATA]')
    cleanContent = parts[0]
    try {
      const jsonStr = parts[1].split('-->')[0].trim()
      infographicsData = JSON.parse(jsonStr)
    } catch (e) {
      console.error('Failed to parse infographics data', e)
    }
  }

  // Render markdown helper
  const renderFormattedMarkdown = (raw: string) => {
    const lines = raw.split('\n')
    return lines.map((line, idx) => {
      if (line.startsWith('# ')) {
        return <h1 key={idx} className="text-xl font-bold text-primary mt-4 mb-2">{line.replace('# ', '')}</h1>
      }
      if (line.startsWith('## ')) {
        return <h2 key={idx} className="text-lg font-semibold text-foreground mt-4 mb-2 border-b border-border pb-1">{line.replace('## ', '')}</h2>
      }
      if (line.startsWith('### ')) {
        return <h3 key={idx} className="text-base font-semibold text-primary mt-3 mb-1">{line.replace('### ', '')}</h3>
      }
      if (line.startsWith('#### ')) {
        return <h4 key={idx} className="text-sm font-semibold text-foreground mt-2 mb-1">{line.replace('#### ', '')}</h4>
      }
      if (line.startsWith('|')) {
        if (line.includes('---')) return null
        const cells = line.split('|').filter(c => c.trim() !== '')
        return (
          <div key={idx} className="grid grid-cols-3 gap-2 p-2 text-xs border-b border-border/50 font-mono bg-muted/10 hover:bg-muted/30">
            {cells.map((cell, i) => (
              <span key={i} className={i === 0 ? 'font-semibold text-foreground' : i === 1 ? 'text-primary font-bold' : 'text-muted-foreground'}>
                {cell.trim().replace(/\*\*/g, '').replace(/`/g, '')}
              </span>
            ))}
          </div>
        )
      }
      if (line.startsWith('- ')) {
        const text = line.replace('- ', '')
        const parts = text.split('**')
        return (
          <li key={idx} className="ml-4 list-disc text-sm text-foreground/90 my-1">
            {parts.map((p, i) => i % 2 === 1 ? <strong key={i} className="font-semibold text-primary">{p}</strong> : p)}
          </li>
        )
      }
      if (line.trim() === '') {
        return <div key={idx} className="h-2" />
      }
      const parts = line.split('**')
      return (
        <p key={idx} className="text-sm text-foreground/90 my-1 leading-relaxed">
          {parts.map((p, i) => i % 2 === 1 ? <strong key={i} className="font-semibold text-foreground">{p}</strong> : p)}
        </p>
      )
    })
  }

  const handleDownloadPDF = async () => {
    if (!html2pdf) return
    setIsGeneratingPdf(true)
    
    // Give state a moment to render the infographics wrapper
    await new Promise(r => setTimeout(r, 200))

    const element = document.getElementById('report-pdf-content')
    if (element) {
      const opt = {
        margin:       [10, 10, 10, 10],
        filename:     `${title.replace(/\s+/g, '_').toLowerCase()}.pdf`,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: true },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
      }
      
      try {
        await html2pdf().set(opt).from(element).save()
      } catch (err) {
        console.error('PDF generation failed:', err)
      }
    }
    
    setIsGeneratingPdf(false)
  }

  return (
    <dialog
      ref={dialogRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-transparent p-4 animate-in fade-in duration-200 backdrop:bg-background/80 backdrop:backdrop-blur-sm m-0 w-screen h-screen"
    >
      <div 
        className="flex flex-col w-full max-w-4xl max-h-[85vh] rounded-xl border border-border bg-card shadow-2xl relative animate-in zoom-in-95 overflow-hidden"
        role="document"
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border p-4 bg-muted/40">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
              <FileText className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
              <span className="text-xs px-2 py-0.5 rounded bg-primary/10 text-primary font-medium">
                Status: {isSubmitted ? 'Under Review' : status}
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          >
            <X className="h-5 w-5" />
            <span className="sr-only">Close</span>
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 bg-background space-y-6" id="report-pdf-content">
          {isGeneratingPdf && infographicsData.length > 0 && (
            <div className="mb-8">
              <h1 className="text-3xl font-extrabold text-center mb-8 pb-4 border-b border-slate-200 text-slate-800 uppercase tracking-widest">{title}</h1>
              <ReportInfographics data={infographicsData} />
            </div>
          )}
          
          {/* Render Main Formatted Summary */}
          <div className="space-y-2">
            {renderFormattedMarkdown(cleanContent)}
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-border p-4 bg-muted/40 flex justify-between items-center">
          <span className="text-xs text-muted-foreground">
            {isSubmitted ? 'PenTest-Vulnerability Assessment published.' : 'Draft Report Preview.'}
          </span>
          <div className="flex items-center gap-3">
            <button
              onClick={handleDownloadPDF}
              disabled={isGeneratingPdf}
              className="inline-flex h-9 items-center justify-center rounded-md border border-primary bg-primary text-primary-foreground px-4 text-sm font-medium transition-colors hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGeneratingPdf ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating PDF...
                </>
              ) : (
                'Download (.pdf)'
              )}
            </button>
            <button
              onClick={onClose}
              disabled={isGeneratingPdf}
              className="inline-flex h-9 items-center justify-center rounded-md border border-input bg-background px-4 text-sm font-medium transition-colors hover:bg-accent disabled:opacity-50"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </dialog>
  )
}
