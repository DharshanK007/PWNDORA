import { CheckCircle2, Play, Circle, ChevronRight } from 'lucide-react'
import type { Scenario } from '@/types/scenario'
import type { SessionStateResponse } from '@/types/session'

interface ObjectiveTrackerProps {
  scenario: Scenario
  session: SessionStateResponse
}

export function ObjectiveTracker({ scenario, session }: ObjectiveTrackerProps) {
  const stages = scenario.stages || []
  return (
    <div className="flex flex-col h-full bg-slate-900 border-l border-slate-800">
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Investigation Objectives</h2>
        <span className="bg-slate-800 text-slate-300 text-xs px-2 py-1 rounded font-medium">
          {session.completed_stages.length} / {stages.length}
        </span>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {stages.map((stage, index) => {
          const isCompleted = session.completed_stages.includes(stage.id)
          const isCurrent = session.current_stage_id === stage.id

          return (
            <div 
              key={stage.id} 
              className={`relative pl-8 ${
                isCompleted ? 'text-slate-400' :
                isCurrent ? 'text-white' : 'text-slate-600'
              }`}
            >
              {/* Timeline connecting line */}
              {index < stages.length - 1 && (
                <div 
                  className={`absolute left-3 top-6 w-0.5 h-[calc(100%+0.5rem)] ${
                    isCompleted ? 'bg-blue-500/30' : 'bg-slate-800'
                  }`} 
                />
              )}

              {/* Status Icon */}
              <div className="absolute left-0 top-1.5 flex items-center justify-center w-6 h-6">
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                ) : isCurrent ? (
                  <Play className="w-5 h-5 text-blue-500 fill-blue-500" />
                ) : (
                  <Circle className="w-5 h-5 text-slate-700" />
                )}
              </div>

              {/* Content */}
              <div className={`p-3 rounded-lg border ${
                isCurrent ? 'bg-blue-500/10 border-blue-500/30' :
                isCompleted ? 'bg-slate-800/50 border-slate-800' :
                'bg-slate-900 border-slate-800'
              }`}>
                <h3 className="font-medium text-sm mb-1 flex items-start justify-between">
                  <span>
                    <span className="text-xs mr-2 opacity-60">Stage {index + 1}</span>
                    {stage.objective}
                  </span>
                  {isCurrent && (
                    <span className="text-[10px] uppercase tracking-wider font-bold text-blue-400 bg-blue-500/20 px-2 py-0.5 rounded ml-2">
                      Active
                    </span>
                  )}
                </h3>
                
                {isCurrent && stage.required_action && (
                  <div className="mt-2 text-xs text-blue-300 flex items-center bg-blue-900/20 p-2 rounded border border-blue-500/20">
                    <ChevronRight className="w-4 h-4 mr-1 flex-shrink-0" />
                    <span>Action Required: {stage.required_action}</span>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
