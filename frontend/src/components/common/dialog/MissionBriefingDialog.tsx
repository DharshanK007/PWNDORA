import { useRef, useEffect } from 'react'
import { X, Target, Crosshair, Fingerprint, Lightbulb, Shield, Code, Key } from 'lucide-react'

interface MissionBriefingDialogProps {
  isOpen: boolean
  onClose: () => void
  scenarioName: string
  stage: any
}

export function MissionBriefingDialog({ isOpen, onClose, scenarioName, stage }: MissionBriefingDialogProps) {
  if (!isOpen || !stage) return null

  return (
    <div
      className="fixed top-32 right-6 z-50 flex flex-col w-full max-w-lg rounded-xl border border-border bg-card shadow-2xl animate-in slide-in-from-right-8 duration-300 overflow-hidden"
    >
      <div className="flex flex-col w-full h-full relative">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border p-4 bg-muted/40">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
              <Target className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h2 className="text-lg font-semibold tracking-tight">Mission Briefing</h2>
              <span className="text-xs text-muted-foreground font-mono">{scenarioName} — Stage {stage.id}</span>
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
        <div className="p-6 space-y-6 text-sm bg-background overflow-y-auto max-h-[70vh] custom-scrollbar">
          
          {/* Objective Banner */}
          <div className="p-4 rounded-lg bg-primary/10 border border-primary/20 space-y-2">
            <div className="flex items-center gap-2 text-primary font-semibold">
              <Crosshair className="h-4 w-4" />
              <span>Stage Objective</span>
            </div>
            <p className="text-foreground leading-relaxed">
              {stage.objective}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 rounded-lg bg-muted/30 border border-border/50 space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground font-semibold text-xs uppercase tracking-wider">
                <Code className="h-3.5 w-3.5" />
                <span>Technical Mechanism</span>
              </div>
              <p className="font-mono text-xs text-foreground">
                {stage.technical_mechanism || stage.vulnerability_category}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-muted/30 border border-border/50 space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground font-semibold text-xs uppercase tracking-wider">
                <Shield className="h-3.5 w-3.5" />
                <span>OWASP Category</span>
              </div>
              <p className="font-mono text-xs text-foreground">
                {stage.owasp || 'N/A'}
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-2 text-muted-foreground font-semibold text-sm border-b border-border pb-2">
              <Lightbulb className="h-4 w-4 text-amber-500" />
              <span>Discovery & Execution Strategy</span>
            </div>
            <p className="text-muted-foreground leading-relaxed">
              {stage.discovery_process}
            </p>
          </div>

          {stage.credentials_to_use && (
            <div className="p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/20 space-y-2">
              <div className="flex items-center gap-2 text-emerald-500 font-semibold">
                <Key className="h-4 w-4" />
                <span>Required Credentials / Input Hint</span>
              </div>
              <p className="text-foreground font-mono text-xs leading-relaxed">
                {stage.credentials_to_use}
              </p>
            </div>
          )}

          <div className="space-y-4">
            <div className="flex items-center gap-2 text-muted-foreground font-semibold text-sm border-b border-border pb-2">
              <Fingerprint className="h-4 w-4 text-primary" />
              <span>Learning Outcome</span>
            </div>
            <p className="text-muted-foreground leading-relaxed italic">
              "{stage.capability_gained}"
            </p>
          </div>

        </div>

        {/* Footer */}
        <div className="border-t border-border p-4 bg-muted/40 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90 font-medium shadow-sm transition-colors"
          >
            Acknowledge
          </button>
        </div>
      </div>
    </div>
  )
}
