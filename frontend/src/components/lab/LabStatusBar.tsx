import { useState, useEffect, useRef } from 'react'
import { Shield, FolderOpen, CheckCircle2, ChevronRight, Flag, Lock, Sparkles, Clock, Trophy, RotateCcw, Target, AlertCircle } from 'lucide-react'
import { useLabSession } from '@/contexts/LabSessionContext'
import { EvidenceDrawer } from './EvidenceDrawer'
import { PostLabAssessmentDialog } from './PostLabAssessmentDialog'
import { MissionBriefingDialog } from '@/components/common/dialog/MissionBriefingDialog'
import api from '@/lib/axios'
import confetti from 'canvas-confetti'

// ─────────────────────────────────────────────────────────────────────────────
// LabStatusBar — fully data-driven from the active scenario YAML.
// No hardcoded stage arrays. Works for any scenario loaded by the engine.
// ─────────────────────────────────────────────────────────────────────────────

export const LabStatusBar: React.FC = () => {
  const { isActive, currentStage, completedStages, status, scenario, state, refetch } = useLabSession()
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [isAssessmentOpen, setIsAssessmentOpen] = useState(false)
  const [showCompletionPopup, setShowCompletionPopup] = useState(false)
  const [isBriefingOpen, setIsBriefingOpen] = useState(false)
  const [briefingSeen, setBriefingSeen] = useState(false)
  const [evidenceSeen, setEvidenceSeen] = useState(false)

  const [timeLeft, setTimeLeft] = useState<number>(45 * 60)
  const [showBanner, setShowBanner] = useState(true)

  useEffect(() => {
    if (state?.id) {
      setBriefingSeen(localStorage.getItem(`briefingSeen_${state.id}`) === 'true')
      setEvidenceSeen(localStorage.getItem(`evidenceSeen_${state.id}`) === 'true')
    } else {
      setBriefingSeen(true)
      setEvidenceSeen(true)
    }
  }, [state?.id])

  const handleBriefingClick = () => {
    setIsDrawerOpen(false)
    setIsBriefingOpen(true)
    if (state?.id) {
      localStorage.setItem(`briefingSeen_${state.id}`, 'true')
      setBriefingSeen(true)
    }
  }

  const handleEvidenceClick = () => {
    setIsBriefingOpen(false)
    setIsDrawerOpen(true)
    if (state?.id) {
      localStorage.setItem(`evidenceSeen_${state.id}`, 'true')
      setEvidenceSeen(true)
    }
  }

  // Derive stages from the live scenario config — works for any scenario
  const stages = scenario?.stages ?? []
  const totalStages = stages.length

  const isCompleted = status === 'COMPLETED'

  // Track transitions to detect when the final stage is captured live
  const prevCompletedCount = useRef(completedStages.length)

  useEffect(() => {
    if (completedStages.length === totalStages && totalStages > 0 && prevCompletedCount.current < totalStages) {
      
      const fireVictory = () => {
        setShowCompletionPopup(true)
        const duration = 3000;
        const end = Date.now() + duration;
        const frame = () => {
          confetti({
            particleCount: 5,
            angle: 60,
            spread: 55,
            origin: { x: 0 },
            colors: ['#10b981', '#3b82f6', '#06b6d4'],
            zIndex: 99999
          });
          confetti({
            particleCount: 5,
            angle: 120,
            spread: 55,
            origin: { x: 1 },
            colors: ['#10b981', '#3b82f6', '#06b6d4'],
            zIndex: 99999
          });
          if (Date.now() < end) {
            requestAnimationFrame(frame);
          }
        };
        frame();
      }

      // Dynamic check: wait until user closes any active sliding panels or dialogs
      const checkAndShow = () => {
        const openDialogs = document.querySelectorAll('dialog[open]')
        if (openDialogs.length > 0) {
          setTimeout(checkAndShow, 500)
        } else {
          fireVictory()
        }
      }
      
      checkAndShow()
    }
    prevCompletedCount.current = completedStages.length
  }, [completedStages.length, totalStages])

  // Timer Logic — 45 minutes from session start
  useEffect(() => {
    const allStagesDone = totalStages > 0 && completedStages.length === totalStages
    if (isActive && state?.started_at && !isCompleted && !allStagesDone) {
      const start = new Date(state.started_at).getTime()
      const maxTime = 45 * 60 * 1000
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
  }, [isActive, state?.started_at, isCompleted, completedStages.length, totalStages])

  // Auto-hide status bar 5s after completion
  useEffect(() => {
    if (isCompleted) {
      const t = setTimeout(() => setShowBanner(false), 5000)
      return () => clearTimeout(t)
    }
  }, [isCompleted])

  if (!isActive) return null

  const displayStage = isCompleted ? totalStages : Math.min(Math.max(currentStage, 1), totalStages)

  // Progress line percentage connecting node centers
  const progressPercent = totalStages <= 1
    ? (isCompleted ? 100 : 0)
    : isCompleted
    ? 100
    : Math.min(100, Math.max(0, ((displayStage - 1) / (totalStages - 1)) * 100))

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }

  // Build the current stage label from scenario data
  const currentStageData = stages.find(s => s.id === displayStage)
  const currentStageName = currentStageData?.objective ?? `Stage ${displayStage}`
  const scenarioName = scenario?.name ?? 'NeoFactory Cyber Range'

  // Build completed stage objects for the assessment dialog
  const completedStageObjects = stages.filter(s => completedStages.includes(s.id))

  return (
    <>
      {(!isCompleted || showBanner) && (
        <div className={`w-full relative z-40 bg-card/95 border-b border-border shadow-md divide-y divide-border/40 transition-all duration-700 ${isCompleted && !showBanner ? 'opacity-0 h-0 overflow-hidden' : 'animate-fade-in'}`}>
          {/* Top Info Strip */}
          <div className="bg-gradient-to-r from-primary/15 via-primary/10 to-background px-4 py-2 flex items-center justify-between text-xs sm:text-sm">
            {/* Left: Status & Stage */}
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary/20 text-primary font-semibold shrink-0">
                <Shield className="h-3.5 w-3.5" />
                <span>{isCompleted ? 'LAB COMPLETED' : `STAGE ${displayStage} / ${totalStages}`}</span>
              </div>

              <div className="flex items-center gap-2 truncate">
                <span className="font-medium text-foreground truncate">
                  {scenarioName}
                </span>
                <ChevronRight className="h-3.5 w-3.5 text-muted-foreground shrink-0 hidden md:inline" />
                <span className="text-muted-foreground truncate hidden md:inline font-mono text-xs">
                  {isCompleted ? 'Scenario Investigation Complete!' : currentStageName}
                </span>
              </div>
            </div>

            {/* Right: Actions */}
            <div className="flex items-center gap-4 pr-8">
              {/* Mission Controls (Primary) */}
              <div className="flex items-center gap-2 bg-background/50 p-1 rounded-lg border border-border/60 shadow-sm">
                <button
                  onClick={handleBriefingClick}
                  className="relative flex items-center gap-1.5 px-4 py-1.5 rounded-md bg-emerald-500/10 border border-emerald-500/20 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 transition-colors font-semibold text-xs"
                >
                  <Target className="h-4 w-4" />
                  <span>MISSION BRIEFING</span>
                  {!briefingSeen && (
                    <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                    </span>
                  )}
                  {!briefingSeen && (
                    <span className="absolute top-[calc(100%+12px)] left-0 right-0 flex justify-center pointer-events-none z-[9999]">
                      <span className="flex flex-col items-center animate-bounce">
                        <span className="w-3 h-3 bg-slate-900 border-l border-t border-emerald-500/30 rotate-45 -mb-1.5 relative z-10 block" />
                        <span className="bg-slate-900 text-emerald-400 border border-emerald-500/30 text-[11px] font-bold px-3 py-1.5 rounded-md shadow-2xl block relative z-20 whitespace-nowrap">
                          Click for mission briefing
                        </span>
                      </span>
                    </span>
                  )}
                </button>

                <button
                  onClick={handleEvidenceClick}
                  className="relative flex items-center gap-1.5 px-4 py-1.5 rounded-md bg-blue-500/10 border border-blue-500/20 hover:bg-blue-500/20 text-blue-600 dark:text-blue-400 transition-colors font-semibold text-xs"
                >
                  <FolderOpen className="h-4 w-4" />
                  <span>ARCHIVES / HINTS</span>
                  {briefingSeen && !evidenceSeen && (
                    <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
                    </span>
                  )}
                  {briefingSeen && !evidenceSeen && (
                    <span className="absolute top-[calc(100%+12px)] left-0 right-0 flex justify-center pointer-events-none z-[9999]">
                      <span className="flex flex-col items-center animate-bounce">
                        <span className="w-3 h-3 bg-slate-900 border-l border-t border-blue-500/30 rotate-45 -mb-1.5 relative z-10 block" />
                        <span className="bg-slate-900 text-blue-400 border border-blue-500/30 text-[11px] font-bold px-3 py-1.5 rounded-md shadow-2xl block relative z-20 whitespace-nowrap">
                          Click for archives & hints
                        </span>
                      </span>
                    </span>
                  )}
                </button>
              </div>

              {/* Separator */}
              <div className="hidden sm:block h-8 w-px bg-border/60 mx-1"></div>

              {/* Timer & Session Actions */}
              <div className="flex items-center gap-3">
                {state?.scenario_id && !isCompleted && (
                  <div className="flex items-center gap-3 bg-background/50 px-3 py-1 rounded-lg border border-border/60 shadow-sm">
                    <div className="flex flex-col items-end">
                      <span className="text-[9px] font-mono text-muted-foreground uppercase tracking-widest leading-none mt-0.5">
                        Time Remaining
                      </span>
                      <div className={`text-sm font-mono font-bold flex items-center gap-1.5 ${
                        timeLeft < 300 ? 'text-red-500 animate-pulse' : 'text-foreground'
                      }`}>
                        <Clock className="h-3.5 w-3.5" />
                        {formatTime(timeLeft)}
                      </div>
                    </div>
                  </div>
                )}

                {isCompleted && (
                  <span className="flex items-center gap-1.5 text-emerald-500 font-bold px-3 py-1.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-xs shadow-sm">
                    <CheckCircle2 className="h-4 w-4" />
                    100% SECURED
                  </span>
                )}

                {!isCompleted && completedStages.length > 0 && (
                  <button
                    onClick={() => setIsAssessmentOpen(true)}
                    className="flex items-center gap-1.5 px-4 py-2 rounded-md bg-secondary border border-border hover:bg-secondary/80 text-foreground font-semibold text-xs shadow-sm transition-colors"
                  >
                    FINISH & EVALUATE
                  </button>
                )}

                {!isCompleted && (
                  <button
                    onClick={async () => {
                      if (state?.scenario_id && confirm('Are you sure you want to end this lab session? All progress will be lost.')) {
                        try {
                          await api.post(`/scenarios/${state.scenario_id}/reset`)
                          refetch()
                        } catch (e) {
                          console.error(e)
                        }
                      }
                    }}
                    className="flex items-center gap-1.5 px-4 py-2 rounded-md bg-red-500/90 hover:bg-red-600 text-white font-bold text-xs shadow-sm transition-all"
                    title="Quit Lab"
                  >
                    <AlertCircle className="h-4 w-4" />
                    <span className="hidden sm:inline">QUIT LAB</span>
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Timeline Bar — fully driven from scenario.stages[] */}
          <div className="px-6 pt-10 pb-3 bg-muted/20 overflow-x-auto">
            <div className="relative max-w-5xl mx-auto" style={{ minWidth: `${Math.max(500, totalStages * 160)}px` }}>
              {/* Background Track */}
              <div className="absolute top-[16px] left-8 right-8 h-1.5 bg-border/60 rounded-full z-0" />

              {/* Dynamic Progress Line */}
              <div
                className="absolute top-[16px] left-8 h-1.5 bg-gradient-to-r from-primary via-emerald-500 to-cyan-400 rounded-full transition-all duration-700 ease-out z-0 shadow-xs"
                style={{ width: `calc(${progressPercent}% * 0.94)` }}
              />

              {/* Stage Nodes */}
              <div className="relative z-10 flex items-center justify-between">
                {stages.map((stage) => {
                  const stageDone = completedStages.includes(stage.id) || isCompleted || displayStage > stage.id
                  const isCurrent = !isCompleted && displayStage === stage.id

                  return (
                    <div key={stage.id} className="flex flex-col items-center relative">
                      {/* Flag icon above node */}
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
                          <CheckCircle2 className="h-4 w-4 stroke-[2.5]" />
                        ) : isCurrent ? (
                          <Sparkles className="h-4 w-4 animate-spin" style={{ animationDuration: '3s' }} />
                        ) : (
                          <Lock className="h-4 w-4 text-muted-foreground/60" />
                        )}
                      </div>

                      {/* Labels Below */}
                      <div className="mt-2 text-center flex flex-col items-center max-w-[110px]">
                        <span
                          className={`text-[10px] font-semibold tracking-tight transition-colors leading-tight ${
                            stageDone ? 'text-foreground font-bold' : isCurrent ? 'text-primary font-bold' : 'text-muted-foreground/70'
                          }`}
                        >
                          Stage {stage.id}
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

      {/* Mission Accomplished Popup */}
      {showCompletionPopup && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in zoom-in duration-500">
          <div className="bg-card w-full max-w-lg rounded-2xl border-2 border-emerald-500 shadow-[0_0_50px_-12px_rgba(16,185,129,0.5)] p-8 text-center flex flex-col items-center mx-4">
            <div className="h-24 w-24 rounded-full bg-emerald-500/20 flex items-center justify-center mb-6 animate-pulse">
               <Trophy className="h-12 w-12 text-emerald-400" />
            </div>
            <h2 className="text-3xl font-black text-foreground mb-2">Mission Accomplished!</h2>
            <p className="text-sm font-mono text-emerald-400 mb-4">{scenarioName}</p>
            <p className="text-muted-foreground mb-8 text-base">
              You have successfully completed all {totalStages} stages. Time to author your PenTest-Vulnerability Assessment.
            </p>
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

      <MissionBriefingDialog
        isOpen={isBriefingOpen}
        onClose={() => setIsBriefingOpen(false)}
        scenarioName={scenarioName}
        stage={currentStageData}
      />

      <PostLabAssessmentDialog
        isOpen={isAssessmentOpen}
        completedStages={completedStageObjects}
        onCancel={() => setIsAssessmentOpen(false)}
        onSubmit={async (answers: any) => {
          setIsAssessmentOpen(false)
          try {
            if (state?.scenario_id) {
              await api.post(`/scenarios/${state.scenario_id}/action`, { action: 'end_session', answers })
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
