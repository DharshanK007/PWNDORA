import React, { useState } from 'react'
import { X, ShieldAlert, CheckCircle2, Lock, FileText, Code, Database, UserCheck, Lightbulb, Eye } from 'lucide-react'
import { useLabSession } from '@/contexts/LabSessionContext'
import api from '@/lib/axios'

interface EvidenceDrawerProps {
  isOpen: boolean
  onClose: () => void
}

const SCENARIO_EVIDENCE_ITEMS: Record<string, any[]> = {
  operation_phantom_firmware: [
    {
      stageId: 1,
      key: 'device_record_line2',
      title: 'Stage 1 Evidence: Line 2 Device Record',
      category: 'Asset Inventory',
      icon: Database,
      description: 'We found the target asset (PLC-Line2-FW-Controller) under maintenance. We can now use its details to search for recent maintenance tickets to see who was assigned to it.',
    },
    {
      stageId: 2,
      key: 'employee_record_leak',
      title: 'Stage 2 Evidence: Engineer Profile Leak',
      category: 'Broken Access Control (IDOR)',
      icon: UserCheck,
      description: 'Marcus Chen - Lead Automation Engineer. With this identity exposed, we can search the Deployment Logs for firmware updates pushed by him.',
    },
    {
      stageId: 3,
      key: 'deploy_log_leak',
      title: 'Stage 3 Evidence: Deployment Audit Logs',
      category: 'Injection / Data Leak',
      icon: Code,
      description: 'System Log #001: Unauthorized firmware update pushed to Production Line 2 by an administrator. This confirms the vulnerability lies in role verification.',
    }
  ],
  silent_exfiltration: [
    {
      stageId: 1,
      key: 'helpdesk_login',
      title: 'Stage 1 Evidence: Helpdesk Compromise',
      category: 'Authentication Flaw',
      icon: UserCheck,
      description: 'Successfully discovered the temporary password pattern (Nf@[year]!) and logged in as jess.okafor. The system failed to enforce rate-limiting after repeated failed attempts.',
    },
    {
      stageId: 2,
      key: 'search_injection',
      title: 'Stage 2 Evidence: Internal Data Leak',
      category: 'Injection',
      icon: Code,
      description: 'Successfully manipulated the global search using SQL injection to uncover internal configuration files.',
    },
    {
      stageId: 3,
      key: 'backup_traversal',
      title: 'Stage 3 Evidence: Internal Credentials Leak',
      category: 'Arbitrary File Read',
      icon: FileText,
      description: 'Successfully exploited a path traversal vulnerability in the backup download feature to access the internal_secrets/svc_credentials.txt file.',
    },
    {
      stageId: 4,
      key: 'authorization_bypass',
      title: 'Stage 4 Evidence: Privilege Escalation',
      category: 'Authorization Bypass',
      icon: ShieldAlert,
      description: 'Successfully utilized the stolen internal service key to bypass administrative access controls and export the employee directory.',
    }
  ]
}

const SCENARIO_STAGE_HINTS: Record<string, Record<number, string[]>> = {
  operation_phantom_firmware: {
    1: [
      "Apply reasonable filters (e.g., Status: Maintenance, Group: Production) in assets to narrow down the list.",
      "Check for the patch date carefully; the targeted asset will be noticeably older than the decoys."
    ],
    2: [
      "Use the assigned job role to search for the employee in the Employees section who is assigned in the Assets section.",
      "Look closely at the internal note in the employee profile. It contains an incident reference and a clue about where the firmware activity was recorded."
    ],
    3: [
      'Use the leaked internal note as your pivot. Search for firmware-related deployment evidence connected to the Line 2 halt and ticket #402.',
      'Probe the Search bar with an injection-style query such as " OR 1=1 -- and watch for deployment audit events that should not be visible to your account.'
    ],
    4: [
      "Intercept the firmware update request using the browser's developer tools.",
      "Modify the X-User-Role header in your request from 'Engineer' to 'Administrator' and resend the request."
    ]
  },
  silent_exfiltration: {
    1: [
      "Focus on the helpdesk account mentioned in the incident context. Recent SSO resets often leave behind temporary credential patterns.",
      "The SSO reset note gives the password pattern, but the year is the missing piece. Check when the SSO upgrade happened and use that year in the temporary password format."
    ],
    2: [
      "Now authenticated as the helpdesk account, probe the search bar with unusual inputs to see if the backend query is safely parameterized.",
      "Try entering a common SQL injection payload like ' OR 1=1 -- to manipulate the backend database query."
    ],
    3: [
      "Start with the backup filename leaked by Search. A normal backup request should retrieve that file only from the device backup area.",
      "Look at the filename parameter in the backup request. If the backend joins that value directly into a file path, traversal sequences may let the request resolve outside the backup directory."
    ],
    4: [
      "Read the exposed credential file like an attacker would. The service key is not just a secret value; its scope tells you which business function it can access.",
      "Try the employee export once as the helpdesk user, then repeat the request with the stolen service credential in the expected service-key header. The weakness is the alternate authorization path."
    ]
  }
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({ isOpen, onClose }) => {
  const { currentStage, completedStages, status, state, scenario, refetch } = useLabSession()
  const [activeTab, setActiveTab] = useState<'evidence' | 'hints'>('evidence')
  const [isRevealing, setIsRevealing] = useState(false)

  if (!isOpen) return null

  const hintsUsed = state?.hints_used || {}

  const handleRevealHint = async (stageId: number) => {
    if (!scenario) return
    setIsRevealing(true)
    try {
      await api.post(`/scenarios/${scenario.id}/hints/reveal?stage_id=${stageId}`)
      await refetch()
    } catch (e) {
      console.error("Failed to reveal hint", e)
    } finally {
      setIsRevealing(false)
    }
  }

  const renderEvidence = () => {
    const evidenceItems = SCENARIO_EVIDENCE_ITEMS[scenario?.id || ''] || []
    
    return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {evidenceItems.length === 0 && (
        <div className="text-center py-8 text-sm text-muted-foreground italic">No evidence items configured for this scenario.</div>
      )}
      {evidenceItems.map((item) => {
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
  )
  }

  const renderHints = () => {
    const hintsObj = SCENARIO_STAGE_HINTS[scenario?.id || ''] || {}
    
    return (
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {[1, 2, 3, 4].map(stageId => {
          const isFutureStage = stageId > currentStage && status !== 'COMPLETED'
          const hints = hintsObj[stageId] || []
          const usedForStage = hintsUsed[stageId.toString()] || []
          const isCurrentStage = stageId === currentStage && status !== 'COMPLETED'

          if (isFutureStage) {
            return (
              <div key={stageId} className="space-y-3 opacity-60">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-sm text-foreground">Stage {stageId} Hints</h3>
                  <Lock className="h-3.5 w-3.5 text-muted-foreground" />
                </div>
                <div className="p-4 rounded-lg border border-border/50 bg-muted/10 flex flex-col items-center justify-center gap-2 text-muted-foreground">
                  <Lock className="h-5 w-5" />
                  <p className="text-xs italic">Reach Stage {stageId} to unlock these hints.</p>
                </div>
              </div>
            )
          }

          return (
            <div key={stageId} className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-sm text-foreground">Stage {stageId} Hints</h3>
                <span className="text-xs font-mono text-muted-foreground">Hints Used: {usedForStage.length}/2</span>
              </div>
              
              <div className="space-y-3">
                {hints.map((hint, idx) => {
                  const isRevealed = usedForStage.includes(idx)
                  
                  if (isRevealed) {
                    return (
                      <div key={idx} className="p-3 rounded-lg border border-yellow-500/30 bg-yellow-500/5 flex gap-3 items-start">
                        <Lightbulb className="h-4 w-4 text-yellow-500 shrink-0 mt-0.5" />
                        <p className="text-sm text-foreground/90">{hint}</p>
                      </div>
                    )
                  }
                  
                  // If not revealed, only allow revealing if it's the current active stage.
                  if (!isCurrentStage) {
                     return (
                       <div key={idx} className="p-3 rounded-lg border border-border/50 bg-muted/20 flex gap-3 items-center text-muted-foreground">
                         <Lock className="h-4 w-4 shrink-0" />
                         <p className="text-sm italic">Hint not used.</p>
                       </div>
                     )
                  }

                  // Only show "Reveal" for the FIRST unrevealed hint to enforce sequence (optional but good UX)
                  const isNextHintToReveal = usedForStage.length === idx
                  if (!isNextHintToReveal) {
                     return (
                       <div key={idx} className="p-3 rounded-lg border border-border/50 bg-muted/20 flex gap-3 items-center text-muted-foreground">
                         <Lock className="h-4 w-4 shrink-0" />
                         <p className="text-sm italic">Unlock Hint {idx} first.</p>
                       </div>
                     )
                  }

                  return (
                    <div key={idx} className="p-3 rounded-lg border border-border bg-card flex gap-3 items-center justify-between">
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <Lock className="h-4 w-4" />
                        <span className="text-sm">Hidden Hint {idx + 1}</span>
                      </div>
                      <button 
                        onClick={() => handleRevealHint(stageId)}
                        disabled={isRevealing}
                        className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium rounded-md bg-secondary hover:bg-secondary/80 text-secondary-foreground transition-colors disabled:opacity-50"
                      >
                        <Eye className="h-3.5 w-3.5" />
                        Reveal
                      </button>
                    </div>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>
    )
  }

  return (
    <div className="fixed inset-0 z-[100] flex justify-end bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-md h-full bg-card border-l border-border shadow-2xl flex flex-col justify-between animate-in slide-in-from-right duration-300">
        {/* Header */}
        <div className="p-4 border-b border-border bg-muted/40 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-primary" />
              <h2 className="font-semibold text-foreground">Scenario Archives & Hints</h2>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          
          <div className="flex p-1 bg-background rounded-lg border border-border">
            <button
              onClick={() => setActiveTab('evidence')}
              className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'evidence' ? 'bg-primary text-primary-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
            >
              Archives
            </button>
            <button
              onClick={() => setActiveTab('hints')}
              className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'hints' ? 'bg-primary text-primary-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
            >
              Hints
            </button>
          </div>
        </div>

        {/* Content */}
        {activeTab === 'evidence' ? renderEvidence() : renderHints()}

        {/* Footer */}
        <div className="p-4 border-t border-border bg-muted/20 flex justify-between items-center text-xs text-muted-foreground">
          <span>Target Scenario: {scenario?.name || 'Unknown Scenario'}</span>
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
