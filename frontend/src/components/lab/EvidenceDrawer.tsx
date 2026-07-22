import React from 'react'
import { X, ShieldAlert, CheckCircle2, Lock, FileText, Code, Database, UserCheck } from 'lucide-react'
import { useLabSession } from '@/contexts/LabSessionContext'

interface EvidenceDrawerProps {
  isOpen: boolean
  onClose: () => void
}

const EVIDENCE_ITEMS = [
  {
    stageId: 1,
    key: 'device_record_line2',
    title: 'Stage 1 Evidence: Line 2 Device Record',
    category: 'Asset Inventory',
    icon: Database,
    description: 'Device: PLC-Line2-FW-Controller | Status: Maintenance | OS: OT-RTOS v1.2.3 (Outdated) | Assigned: Marcus Chen',
  },
  {
    stageId: 2,
    key: 'employee_record_leak',
    title: 'Stage 2 Evidence: Engineer Profile Leak',
    category: 'Broken Access Control (IDOR)',
    icon: UserCheck,
    description: 'Marcus Chen - Lead Automation Engineer | Phone: +15550192834 | Note: Check deployment logs via Search bar using firmware query.',
  },
  {
    stageId: 3,
    key: 'deploy_log_leak',
    title: 'Stage 3 Evidence: Deployment Audit Logs',
    category: 'Injection / Data Leak',
    icon: Code,
    description: 'System Log #001: Unauthorized firmware update pushed to Production Line 2 by session with overridden X-User-Role: Administrator.',
  },
  {
    stageId: 4,
    key: 'session_escalation_proof',
    title: 'Stage 4 Evidence: Privilege Escalation Proof',
    category: 'Client Trust / Authentication',
    icon: FileText,
    description: 'Confirmed Root Cause: Firmware push endpoint trusted client-supplied role header X-User-Role without server-side verification.',
  },
]

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({ isOpen, onClose }) => {
  const { currentStage, completedStages, status } = useLabSession()

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-md h-full bg-card border-l border-border shadow-2xl flex flex-col justify-between animate-in slide-in-from-right duration-300">
        {/* Header */}
        <div className="p-4 border-b border-border flex items-center justify-between bg-muted/40">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-5 w-5 text-primary" />
            <h2 className="font-semibold text-foreground">Scenario Evidence & Clues</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {EVIDENCE_ITEMS.map((item) => {
            const isUnlocked = completedStages.includes(item.stageId) || (status === 'COMPLETED' || currentStage > item.stageId)
            const Icon = item.icon

            const containerClass = isUnlocked
              ? 'p-4 rounded-xl border transition-all border-primary/40 bg-primary/5 text-foreground shadow-sm'
              : 'p-4 rounded-xl border transition-all border-border/60 bg-muted/20 text-muted-foreground opacity-75'

            const iconClass = isUnlocked ? 'p-2 rounded-lg bg-primary/20 text-primary' : 'p-2 rounded-lg bg-muted text-muted-foreground'

            return (
              <div key={item.key} className={containerClass}>
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <div className={iconClass}>
                      <Icon className="h-4 w-4" />
                    </div>
                    <div>
                      <h3 className="font-medium text-sm text-foreground">{item.title}</h3>
                      <span className="text-xs text-muted-foreground">{item.category}</span>
                    </div>
                  </div>
                  {isUnlocked ? (
                    <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0 mt-1" />
                  ) : (
                    <Lock className="h-4 w-4 text-muted-foreground shrink-0 mt-1" />
                  )}
                </div>

                <div className="mt-3 pt-3 border-t border-border/40 text-xs leading-relaxed font-mono">
                  {isUnlocked ? (
                    <span className="text-foreground/90">{item.description}</span>
                  ) : (
                    <span className="italic text-muted-foreground">Locked — Complete Stage {item.stageId} to unlock evidence.</span>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border bg-muted/20 flex justify-between items-center text-xs text-muted-foreground">
          <span>Target Scenario: Operation Phantom Firmware</span>
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80 font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}
