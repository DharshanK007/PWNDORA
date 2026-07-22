import { useEffect, useMemo } from 'react'
import { useSearchParams, Navigate, Link } from 'react-router-dom'
import { useScenarios } from '@/hooks/api/useScenarios'
import { useCurrentSession, useWorkspace, usePerformAction } from '@/hooks/api/useSession'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'

// Components
import { WorkspaceHeader } from '@/components/workspace/WorkspaceHeader'
import { WorkspaceToolbar } from '@/components/workspace/WorkspaceToolbar'
import { EvidenceExplorer } from '@/components/workspace/EvidenceExplorer'
import { FileViewer } from '@/components/workspace/FileViewer'
import { NotesPanel } from '@/components/workspace/NotesPanel'
import { ObjectiveTracker } from '@/components/workspace/ObjectiveTracker'
import { LogViewer } from '@/components/workspace/LogViewer'
import { TimelinePanel } from '@/components/workspace/TimelinePanel'

// Types
import type { Evidence } from '@/types/workspace'

// Simulated Evidence for this milestone
const SIMULATED_EVIDENCE: Record<string, Evidence[]> = {
  'scenario_001': [
    { id: 'ev_1', name: 'ticket_001.txt', type: 'text', size: 1024, source: 'IT Helpdesk', addedAt: new Date().toISOString(), content: 'Ticket 001\nPriority: High\nDescription: Production line 2 firmware update failed. Line is stopped.' },
    { id: 'ev_2', name: 'deploy_log_001.log', type: 'log', size: 4096, source: 'Deploy Server', addedAt: new Date().toISOString(), content: '2026-07-21 08:00:01 INFO Starting firmware deployment to Line 2\n2026-07-21 08:00:15 INFO Uploading binary...\n2026-07-21 08:00:16 ERROR Checksum mismatch! Deployment aborted.\n2026-07-21 08:00:16 ERROR Fallback to config_backup.json failed (Permission Denied).' },
    { id: 'ev_3', name: 'config_backup.json', type: 'json', size: 2048, source: 'File Server', addedAt: new Date().toISOString(), content: '{\n  "admin_endpoint": "/auth/login",\n  "default_user": "admin",\n  "default_pass": "admin123"\n}' },
    { id: 'ev_4', name: 'network_capture.pcap', type: 'pcap', size: 1548288, source: 'Edge Router', addedAt: new Date().toISOString() },
    { id: 'ev_5', name: 'engineer_profile.json', type: 'json', size: 512, source: 'HR System API', addedAt: new Date().toISOString(), content: '{\n  "id": "eng_882",\n  "department": "Engineering",\n  "access_level": "Tier 2",\n  "managed_devices": ["PLC_Line2"]\n}' },
  ]
}

// Simulated Logs for this milestone
const SIMULATED_LOGS = [
  { id: 'log1', timestamp: new Date(Date.now() - 5000).toISOString(), level: 'INFO' as const, source: 'System', message: 'Workspace initialized.' },
  { id: 'log2', timestamp: new Date(Date.now() - 4000).toISOString(), level: 'INFO' as const, source: 'ScenarioManager', message: 'Scenario environment provisioned.' },
  { id: 'log3', timestamp: new Date(Date.now() - 3000).toISOString(), level: 'WARN' as const, source: 'Monitor', message: 'High CPU usage detected on simulated endpoint.' },
]

export function InvestigationWorkspace() {
  const [searchParams] = useSearchParams()
  const scenarioId = searchParams.get('scenarioId')

  // Queries
  const { data: scenarios, isLoading: isLoadingScenarios } = useScenarios()
  const scenario = useMemo(() => scenarios?.find(s => s.id === scenarioId), [scenarios, scenarioId])
  
  const { data: session, isLoading: isLoadingSession } = useCurrentSession(scenarioId || '')
  const { workspace, updateWorkspace, addTimelineEvent, resetWorkspace } = useWorkspace(scenarioId || '')
  const performAction = usePerformAction()

  // Effect to add initial timeline event
  useEffect(() => {
    if (session && workspace.timeline.length === 0) {
      addTimelineEvent({
        type: 'INFO',
        message: 'Investigation started'
      })
    }
  }, [session, workspace.timeline.length]) // eslint-disable-line react-hooks/exhaustive-deps

  if (!scenarioId) {
    return (
      <div className="h-screen w-full flex flex-col items-center justify-center bg-[#0a0a0a] text-slate-400">
        <div className="w-16 h-16 border-2 border-dashed border-slate-700 rounded-lg mb-4 flex items-center justify-center">
          <span className="text-2xl">🔍</span>
        </div>
        <h2 className="text-xl font-semibold text-slate-200 mb-2">No Active Investigation</h2>
        <p className="text-sm mb-6 max-w-md text-center">
          You haven't selected a scenario to investigate. Please go to the Scenario Catalog, select a scenario, and launch it to begin an investigation session.
        </p>
        <Link 
          to="/scenarios"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-md transition-colors text-sm font-medium"
        >
          Go to Scenario Catalog
        </Link>
      </div>
    )
  }
  if (isLoadingScenarios || isLoadingSession) return <div className="h-screen w-full flex items-center justify-center bg-[#0a0a0a]"><LoadingSpinner /></div>
  if (!scenario || !session) return <Navigate to="/scenarios" replace /> // Missing scenario or session not started

  const evidence = SIMULATED_EVIDENCE[scenarioId] || []
  const selectedEvidence = evidence.find(e => e.id === workspace.selectedEvidenceId) || null

  return (
    <div className="h-screen w-full flex flex-col bg-[#0a0a0a] overflow-hidden">
      <WorkspaceHeader scenario={scenario} session={session} />
      <WorkspaceToolbar 
        scenarioId={scenarioId}
        onResetLayout={resetWorkspace}
        onSaveNotes={() => {
          addTimelineEvent({ type: 'SUCCESS', message: 'Notes force saved' })
        }}
      />

      {/* Main Split Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel: Explorer & Notes */}
        <div style={{ width: `${workspace.layout.sizes.left}%` }} className="flex flex-col border-r border-slate-800">
          <div className="flex-1 overflow-hidden">
            <EvidenceExplorer 
              evidence={evidence} 
              selectedId={workspace.selectedEvidenceId}
              onSelect={(id) => {
                updateWorkspace({ selectedEvidenceId: id })
                addTimelineEvent({ type: 'INFO', message: `Opened evidence: ${evidence.find(e => e.id === id)?.name}` })
                
                // Trigger backend action if relevant
                if (id === 'ev_1') {
                  performAction.mutate({ scenarioId: scenarioId!, action: 'view_ticket_with_sensitive_log' })
                } else if (id === 'ev_5') {
                  performAction.mutate({ scenarioId: scenarioId!, action: 'idor_cross_department' })
                } else if (id === 'ev_3') {
                  performAction.mutate({ scenarioId: scenarioId!, action: 'read_device_config_with_creds' })
                } else if (id === 'ev_4') {
                  performAction.mutate({ scenarioId: scenarioId!, action: 'login_enumeration' })
                }
              }}
            />
          </div>
          <div className="h-[40%] min-h-[200px] border-t border-slate-800">
            <NotesPanel 
              initialNotes={workspace.notes} 
              onChange={(notes) => updateWorkspace({ notes })} 
            />
          </div>
        </div>

        {/* Center Panel: File Viewer & Logs */}
        <div className="flex-1 flex flex-col min-w-0">
          <div className="flex-1 overflow-hidden" style={{ height: `${100 - workspace.layout.sizes.bottom}%` }}>
            <FileViewer file={selectedEvidence} />
          </div>
          <div style={{ height: `${workspace.layout.sizes.bottom}%` }} className="border-t border-slate-800">
            <LogViewer logs={SIMULATED_LOGS} />
          </div>
        </div>

        {/* Right Panel: Tracker & Timeline */}
        <div style={{ width: `${workspace.layout.sizes.right}%` }} className="flex flex-col border-l border-slate-800">
          <div className="flex-1 overflow-hidden">
            <ObjectiveTracker scenario={scenario} session={session} />
          </div>
          <div className="h-[40%] min-h-[200px] border-t border-slate-800">
            <TimelinePanel events={workspace.timeline} />
          </div>
        </div>
      </div>
    </div>
  )
}
