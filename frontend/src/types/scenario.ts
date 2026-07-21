export interface ScenarioStage {
  id: number
  objective: string
  required_action: string
  next_stage: number | null
}

export interface Scenario {
  id: string
  title: string
  description: string
  difficulty: string
  category: string
  
  // Backend raw data mapped to interface
  name?: string
  business_context?: string
  required_role?: string
  stages?: ScenarioStage[]

  // Frontend extensions / defaults
  estimatedTime?: string
  status?: 'Not Started' | 'In Progress' | 'Completed'
  completionPercentage?: number
  tags?: string[]
  author?: string
  createdAt?: string
  updatedAt?: string
  prerequisites?: string[]
  skills?: string[]
  objectives?: string[]
  icon?: string
}

export interface ScenarioState {
  id: string
  scenario_id: string
  user_id: string
  status: 'IN_PROGRESS' | 'COMPLETED' | 'FAILED'
  current_stage: number
  started_at: string
  completed_at: string | null
  score: number
}
