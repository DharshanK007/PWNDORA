import { useState, useEffect, useRef } from 'react'
import { Shield, FolderOpen, CheckCircle2, ChevronRight, Flag, Lock, Sparkles, Clock, Trophy } from 'lucide-react'
import { useLabSession } from '@/contexts/LabSessionContext'
import { EvidenceDrawer } from './EvidenceDrawer'
import { PostLabAssessmentDialog } from './PostLabAssessmentDialog'
import api from '@/lib/axios'

const STAGE_TITLES: Record<number, string> = {
  1: 'Stage 1: Read Device Record for Production Line 2 in Assets',
  2: 'Stage 2: Access Marcus Chen Employee Profile in Employees',
  3: 'Stage 3: Perform Injection Search for Deployment Logs',
  4: 'Stage 4: Escalate Session Role & Execute Firmware Push',
}

const STAGES_CONFIG = [
  {
    id: 1,
    title: 'Asset Triage',
    vuln: 'Asset Inventory',
    target: 'Line 2 Controller',
    flagLabel: 'Flag 1: Asset Discovered',
  },
  {
    id: 2,
    title: 'Access Control',
    vuln: 'OWASP A01: IDOR',
    target: 'Marcus Chen Profile',
    flagLabel: 'Flag 2: Engineer Leaked',
  },
  {
    id: 3,
    title: 'Injection Leak',
    vuln: 'OWASP A03: Injection',
    target: 'Deployment Audit Logs',
    flagLabel: 'Flag 3: Audit Logs Exposed',
  },
  {
    id: 4,
    title: 'Privilege Escalation',
    vuln: 'OWASP A07: Session Esc',
    target: 'Firmware Push Override',
    flagLabel: 'Flag 4: Root Compromised',
  },
]

export const LabStatusBar: React.FC = () => {
  const { isActive, currentStage, completedStages, status, scenario, state, refetch } = useLabSession()
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [isAssessmentOpen, setIsAssessmentOpen] = useState(false)
  const [showCompletionPopup, setShowCompletionPopup] = useState(false)
  
  const [timeLeft, setTimeLeft] = useState<number>(45 * 60)
  const [showBanner, setShowBanner] = useState(true)

  
  const isCompleted = status === 'COMPLETED'
  
  const prevCompletedCount = useRef(completedStages.length)
  
  // Trigger Big Pop Up when the 4th stage is captured live
  useEffect(() => {
    if (completedStages.length === 4 && prevCompletedCount.current < 4) {
      setShowCompletionPopup(true)
    }
    prevCompletedCount.current = completedStages.length
  }, [completedStages.length])
  
  // Timer Logic
  useEffect(() => {
    if (isActive && state?.started_at && !isCompleted) {
      const start = new Date(state.started_at).getTime()
      const maxTime = 45 * 60 * 1000 // 45 mins
      const interval = setInterval(() => {
        const now = Date.now()
        const elapsed = now - start
        const remaining = Math.max(0, Math.floor((maxTime - elapsed) / 1000))
        setTimeLeft(remaining)
        if (remaining === 0) {
          setIsAssessmentOpen(true)
          clearInterval(interval)
        }
      }, 1000)
      return () => clearInterval(interval)
    }
  }, [isActive, state?.started_at, isCompleted])
  
  // Auto-hide banner after 5s when completed
  useEffect(() => {
    if (isCompleted) {
      const t = setTimeout(() => setShowBanner(false), 5000)
      return () => clearTimeout(t)
    }
  }, [isCompleted])

  if (!isActive) return null
  const displayStage = isCompleted ? 4 : Math.min(Math.max(currentStage, 1), 4)

  // Calculate percentage of progress line connecting node centers (0% to 100%)
  const progressPercent = isCompleted
    ? 100
    : Math.min(100, Math.max(0, ((displayStage - 1) / (STAGES_CONFIG.length - 1)) * 100))

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }

  return (
    <>
      {(!isCompleted || showBanner) && (
      <div className={`w-full bg-card/95 border-b border-border shadow-md divide-y divide-border/40 transition-all duration-700 ${isCompleted && !showBanner ? 'opacity-0 h-0 overflow-hidden' : 'animate-fade-in'}`}>
        {/* Top Info Strip */}
        <div className="bg-gradient-to-r from-primary/15 via-primary/10 to-background px-4 py-2 flex items-center justify-between text-xs sm:text-sm">
          {/* Left: Status & Stage */}
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary/20 text-primary font-semibold shrink-0">
              <Shield className="h-3.5 w-3.5" />
              <span>{isCompleted ? 'LAB COMPLETED' : 'STAGE ' + displayStage + ' / 4'}</span>
            </div>

            <div className="flex items-center gap-2 truncate">
              <span className="font-medium text-foreground truncate">
                {scenario?.name || 'Operation Phantom Firmware'}
              </span>
              <ChevronRight className="h-3.5 w-3.5 text-muted-foreground shrink-0 hidden md:inline" />
              <span className="text-muted-foreground truncate hidden md:inline font-mono text-xs">
                {isCompleted ? 'Scenario Investigation Complete!' : STAGE_TITLES[displayStage]}
              </span>
            </div>
          </div>

          {/* Right: Actions */}
          <div className="flex items-center gap-2 shrink-0">
            {!isCompleted && (
              <div className={`flex items-center gap-1.5 px-3 py-1 rounded-md font-mono text-xs font-semibold shadow-xs ${
                timeLeft < 300 ? 'bg-destructive/10 text-destructive border border-destructive/20 animate-pulse' : 'bg-muted/50 text-foreground border border-border'
              }`}>
                <Clock className="h-3.5 w-3.5" />
                {formatTime(timeLeft)}
              </div>
            )}

            {isCompleted && (
              <span className="flex items-center gap-1 text-emerald-500 font-medium px-2 py-0.5 rounded bg-emerald-500/10 text-xs">
                <CheckCircle2 className="h-3.5 w-3.5" />
                100% Score
              </span>
            )}

            {!isCompleted && completedStages.length > 0 && (
              <button
                onClick={() => setIsAssessmentOpen(true)}
                className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-destructive/10 border border-destructive/20 hover:bg-destructive/20 text-destructive font-medium text-xs shadow-xs transition-colors"
              >
                End Session
              </button>
            )}

            <button
              onClick={() => setIsDrawerOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-card border border-border hover:bg-muted text-foreground transition-colors font-medium text-xs shadow-xs"
            >
              <FolderOpen className="h-3.5 w-3.5 text-primary" />
              <span>Evidence</span>
            </button>
          </div>
        </div>

        {/* Timeline Bar with Pinned Stage Flags */}
        <div className="px-6 pt-10 pb-3 bg-muted/20 overflow-x-auto">
          <div className="relative max-w-5xl mx-auto min-w-[650px]">
            {/* Background Track Line - Positioned precisely behind 32px node center */}
            <div className="absolute top-[16px] left-8 right-8 h-1.5 bg-border/60 rounded-full z-0" />

            {/* Dynamic Progress Line - Positioned precisely behind 32px node center */}
            <div
              className="absolute top-[16px] left-8 h-1.5 bg-gradient-to-r from-primary via-emerald-500 to-cyan-400 rounded-full transition-all duration-700 ease-out z-0 shadow-xs"
              style={{ width: `calc(${progressPercent}% * 0.94)` }}
            />

            {/* 4 Stage Nodes with Pinned Flags Above */}
            <div className="relative z-10 flex items-center justify-between">
              {STAGES_CONFIG.map((stage) => {
                const stageDone = completedStages.includes(stage.id) || isCompleted || displayStage > stage.id
                const isCurrent = !isCompleted && displayStage === stage.id

                return (
                  <div key={stage.id} className="flex flex-col items-center relative">
                    {/* Pinned Flag Symbol (Icon Only - Large, Crisp, No Text, No Pill Overlaps) */}
                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 flex items-center justify-center">
                      <Flag
                        className={`transition-all duration-500 transform ${
                          stageDone
                            ? 'h-6 w-6 text-emerald-400 fill-emerald-400 drop-shadow-md -translate-y-1'
                            : isCurrent
                            ? 'h-6 w-6 text-primary fill-primary drop-shadow-lg animate-bounce'
                            : 'h-4 w-4 text-muted-foreground/30 fill-none'
                        }`}
                      />
                    </div>

                    {/* Node Circle */}
                    <div
                      className={`h-8 w-8 rounded-full flex items-center justify-center transition-all duration-500 z-10 ${
                        stageDone
                          ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/30 ring-4 ring-emerald-500/20'
                          : isCurrent
                          ? 'bg-primary text-primary-foreground shadow-lg shadow-primary/30 ring-4 ring-primary/20 scale-105'
                          : 'bg-card border-2 border-border text-muted-foreground'
                      }`}
                    >
                      {stageDone ? (
                        <CheckCircle2 className="h-4.5 w-4.5 stroke-[2.5]" />
                      ) : isCurrent ? (
                        <Sparkles className="h-4 w-4 animate-spin duration-3000" />
                      ) : (
                        <Lock className="h-4 w-4 text-muted-foreground/60" />
                      )}
                    </div>

                    {/* Node Labels Below */}
                    <div className="mt-2 text-center flex flex-col items-center">
                      <span
                        className={`text-xs font-semibold tracking-tight transition-colors ${
                          stageDone ? 'text-foreground font-bold' : isCurrent ? 'text-primary font-bold' : 'text-muted-foreground/70'
                        }`}
                      >
                        {stage.title}
                      </span>
                      <span className="text-[10px] font-mono text-muted-foreground/70 mt-0.5">
                        {stage.vuln}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
      )}

      {showCompletionPopup && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in zoom-in duration-500">
          <div className="bg-card w-full max-w-lg rounded-2xl border-2 border-emerald-500 shadow-[0_0_50px_-12px_rgba(16,185,129,0.5)] p-8 text-center flex flex-col items-center mx-4">
            <div className="h-24 w-24 rounded-full bg-emerald-500/20 flex items-center justify-center mb-6 animate-pulse">
               <Trophy className="h-12 w-12 text-emerald-400" />
            </div>
            <h2 className="text-3xl font-black text-foreground mb-4">Mission Accomplished!</h2>
            <p className="text-muted-foreground mb-8 text-lg">You have successfully compromised all targets in Operation Phantom Firmware.</p>
            <button 
              onClick={() => {
                setShowCompletionPopup(false)
                setIsAssessmentOpen(true)
              }} 
              className="bg-emerald-500 text-white px-8 py-3 rounded-xl font-bold text-lg hover:bg-emerald-600 transition-colors w-full shadow-lg hover:shadow-emerald-500/25"
            >
              Proceed to Vulnerability Assessment
            </button>
          </div>
        </div>
      )}

      <EvidenceDrawer isOpen={isDrawerOpen} onClose={() => setIsDrawerOpen(false)} />
      
      <PostLabAssessmentDialog 
        isOpen={isAssessmentOpen}
        completedStages={STAGES_CONFIG.filter(s => completedStages.includes(s.id))}
        onCancel={() => setIsAssessmentOpen(false)}
        onSubmit={async () => {
          setIsAssessmentOpen(false)
          try {
            // Ideally we could pass the answers to the backend, but the backend natively scores from YAML.
            // For now we just end the session. 
            if (scenario) {
               await api.post(`/scenarios/${scenario.id}/action`, { action: 'end_session' })
               refetch()
            }
          } catch (e) {
            console.error(e)
          }
        }}
      />
    </>
  )
}
