import { Clock, Shield, Target, Activity } from 'lucide-react'
import type { Scenario } from '@/types/scenario'
import type { SessionStateResponse } from '@/types/session'
import { DifficultyBadge } from '@/components/scenarios/DifficultyBadge'
import { useEffect, useState } from 'react'

interface WorkspaceHeaderProps {
  scenario: Scenario
  session: SessionStateResponse
}

export function WorkspaceHeader({ scenario, session }: WorkspaceHeaderProps) {
  const [elapsed, setElapsed] = useState<string>('00:00:00')

  useEffect(() => {
    if (!session.started_at) return
    const start = new Date(session.started_at).getTime()
    
    const interval = setInterval(() => {
      const now = new Date().getTime()
      const diff = now - start
      
      const hours = Math.floor(diff / (1000 * 60 * 60))
      const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      const secs = Math.floor((diff % (1000 * 60)) / 1000)
      
      setElapsed(
        `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      )
    }, 1000)

    return () => clearInterval(interval)
  }, [session.started_at])

  const stages = scenario.stages || []
  const progressPct = stages.length > 0 ? Math.round((session.completed_stages.length / stages.length) * 100) : 0

  return (
    <div className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center space-x-6">
        <div>
          <h1 className="text-xl font-semibold text-white flex items-center">
            <Shield className="w-5 h-5 text-blue-500 mr-2" />
            {scenario.title}
          </h1>
          <div className="flex items-center space-x-3 mt-1 text-sm text-slate-400">
            <DifficultyBadge difficulty={scenario.difficulty} />
            <span>•</span>
            <span className="flex items-center">
              <Target className="w-4 h-4 mr-1" />
              {scenario.category}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-8">
        <div className="flex flex-col items-end">
          <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold mb-1">
            Progress
          </span>
          <div className="flex items-center space-x-3">
            <div className="w-32 bg-slate-800 h-2 rounded-full overflow-hidden">
              <div 
                className="bg-blue-500 h-full transition-all duration-500" 
                style={{ width: `${progressPct}%` }}
              />
            </div>
            <span className="text-sm font-medium text-slate-200">{progressPct}%</span>
          </div>
        </div>

        <div className="flex flex-col items-end">
          <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold mb-1">
            Elapsed Time
          </span>
          <div className="flex items-center text-blue-400 font-mono font-medium">
            <Clock className="w-4 h-4 mr-2" />
            {elapsed}
          </div>
        </div>
        
        <div className="flex flex-col items-end">
          <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold mb-1">
            Status
          </span>
          <div className="flex items-center text-emerald-400 text-sm font-medium">
            <Activity className="w-4 h-4 mr-1" />
            {session.status.replace('_', ' ')}
          </div>
        </div>
      </div>
    </div>
  )
}
