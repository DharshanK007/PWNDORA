import { useEffect, useRef, useState } from 'react'
import { X, FileText, Send, CheckCircle2 } from 'lucide-react'
import api from '@/lib/axios'

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
  
  const [analystNotes, setAnalystNotes] = useState('')
  const [recommendations, setRecommendations] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(status === 'Under Review' || status === 'Approved' || status === 'Published')

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

  const handleSubmitForReview = async () => {
    if (!reportId) return
    setIsSubmitting(true)
    try {
      let updatedContent = content
      if (analystNotes.trim()) {
        updatedContent = updatedContent.replace('[Write your technical analysis here]', analystNotes)
      }
      if (recommendations.trim()) {
        updatedContent = updatedContent.replace('[Write remediation recommendations here]', recommendations)
      }

      await api.patch('/reports/' + reportId + '/submit', {
        summary: updatedContent,
        status: 'Under Review'
      })

      setIsSubmitted(true)
      if (onSaved) onSaved()
    } catch (err) {
      console.error('Failed to submit report:', err)
      alert('Failed to submit report. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
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
        <div className="flex-1 overflow-y-auto p-6 bg-background space-y-6">
          {/* Render Main Formatted Summary */}
          <div className="space-y-2">
            {renderFormattedMarkdown(content)}
          </div>

          {/* Interactive Learner Assessment Questions */}
          <div className="mt-6 border-t border-border pt-6 space-y-5 bg-muted/20 p-5 rounded-xl border border-border/60">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                <FileText className="h-4 w-4 text-primary" />
                <span>Learner Assessment & Report Deliverable Submission</span>
              </h3>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-primary/10 text-primary font-medium">
                Plain English Evaluation
              </span>
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">
              Complete your technical assessment deliverable by evaluating the findings below in plain English. Your responses demonstrate your ability to translate technical exploitation into executive and engineering guidance.
            </p>

            {/* Field 1: Executive Impact Summary */}
            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-foreground">
                1. Executive Impact Summary <span className="text-muted-foreground font-normal">(Plain English for C-Suite Stakeholders)</span>
              </label>
              <textarea
                value={analystNotes}
                onChange={(e) => setAnalystNotes(e.target.value)}
                disabled={isSubmitted}
                placeholder="Summarize the attack impact on Production Line 2 and overall business risk for NeoFactory executive management..."
                className="w-full h-24 p-3 rounded-lg border border-input bg-background text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-60 font-sans"
              />
            </div>

            {/* Field 2: Technical Attack Chain Narrative */}
            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-foreground">
                2. Technical Attack Chain Narrative & Root Cause Analysis
              </label>
              <textarea
                value={recommendations}
                onChange={(e) => setRecommendations(e.target.value)}
                disabled={isSubmitted}
                placeholder="Detail how you exploited Asset Triage -> IDOR Employee Leak -> Search Query Injection -> Client Trust Firmware Push..."
                className="w-full h-24 p-3 rounded-lg border border-input bg-background text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-60 font-sans"
              />
            </div>

            {/* Field 3: Remediation Guidance */}
            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-foreground">
                3. Remediation & Enterprise Security Control Roadmap
              </label>
              <textarea
                disabled={isSubmitted}
                placeholder="Detail concrete architectural fixes: Server-side role enforcement, parameterized SQL queries, IDOR access controls..."
                className="w-full h-24 p-3 rounded-lg border border-input bg-background text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-60 font-sans"
              />
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-border p-4 bg-muted/40 flex justify-between items-center">
          <span className="text-xs text-muted-foreground">
            {isSubmitted ? 'Assessment Report submitted and published.' : 'Complete plain English questions before submitting for review.'}
          </span>
          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="inline-flex h-9 items-center justify-center rounded-md border border-input bg-background px-4 text-sm font-medium transition-colors hover:bg-accent"
            >
              Close
            </button>
            {!isSubmitted && (
              <button
                onClick={handleSubmitForReview}
                disabled={isSubmitting}
                className="inline-flex h-9 items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-50 shadow-sm"
              >
                {isSubmitting ? (
                  'Submitting Deliverable...'
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    Submit Assessment Deliverable
                  </>
                )}
              </button>
            )}
            {isSubmitted && (
              <span className="inline-flex items-center gap-1.5 text-xs text-emerald-500 font-semibold px-3 py-1.5 rounded-md bg-emerald-500/10 border border-emerald-500/20">
                <CheckCircle2 className="h-4 w-4" />
                Pentest Deliverable Submitted & Approved
              </span>
            )}
          </div>
        </div>
      </div>
    </dialog>
  )
}
