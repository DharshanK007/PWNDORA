import type { Scenario } from './scenario'

export type SessionStatus = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED'

export interface ScenarioSession {
  id: string
  scenarioId: string
  status: SessionStatus
  startedAt: string
  updatedAt: string
  completedStages: number[]
  totalStages: number
  currentStageId: number
  
  // Enriched frontend fields
  scenario?: Scenario
}

export interface SessionStateResponse {
  id: string
  scenario_id: string
  user_id: string
  status: SessionStatus
  started_at: string
  updated_at: string
  completed_stages: number[]
  current_stage_id: number
  score: number
  flags_captured: string[]
}
