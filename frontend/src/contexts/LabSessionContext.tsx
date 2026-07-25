import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import api from '@/lib/axios'
import { useAuth } from '@/hooks/useAuth'

// ─── Types ───────────────────────────────────────────────────────────────────
interface ScenarioStage {
  id: number
  title?: string
  objective?: string
  vulnerability_category?: string
  owasp?: string
  mitre?: string
  mitre_techniques?: string[]
  cvss?: Record<string, string>
  enterprise_layer?: string
  attack_surface?: string
  technical_mechanism?: string
  discovery_surface?: string
  next_stage?: number | null
}

interface ScenarioConfig {
  id: string
  name: string
  business_context?: string
  difficulty?: string
  stages: ScenarioStage[]
}

interface ScenarioState {
  id: string
  scenario_id: string
  user_id: string
  current_stage: number
  completed_stages: (string | number)[]
  status: string
  started_at: string
  completed_at?: string | null
  hints_used?: Record<string, number[]>
}

interface LabSessionContextType {
  isActive: boolean
  currentStage: number
  completedStages: (string | number)[]
  status: 'IN_PROGRESS' | 'COMPLETED' | 'NOT_STARTED' | string
  scenario: ScenarioConfig | null
  state: ScenarioState | null
  refetch: () => Promise<void>
}

// ─── Context ─────────────────────────────────────────────────────────────────
const LabSessionContext = createContext<LabSessionContextType | undefined>(undefined)

export const LabSessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth()
  const [state, setState] = useState<ScenarioState | null>(null)
  const [scenario, setScenario] = useState<ScenarioConfig | null>(null)

  const fetchSession = useCallback(async () => {
    try {
      // Poll the generic active-state endpoint — returns whichever scenario is currently IN_PROGRESS
      // or the most recently COMPLETED one. No hardcoded scenario ID.
      const res = await api.get('/scenarios/active-state')
      const data = res.data
      if (data?.state) {
        setState(data.state)
      } else {
        setState(null)
      }
      if (data?.scenario) {
        setScenario(data.scenario)
      } else {
        setScenario(null)
      }
    } catch {
      // Ignore polling errors silently
    }
  }, [])

  useEffect(() => {
    fetchSession()
    const interval = setInterval(fetchSession, 3000)
    return () => clearInterval(interval)
  }, [fetchSession])

  const isActive = state?.status === 'IN_PROGRESS' || state?.status === 'COMPLETED'
  const currentStage = state?.current_stage ?? 1
  const completedStages = state?.completed_stages ?? []
  const status = state?.status ?? 'NOT_STARTED'

  return (
    <LabSessionContext.Provider
      value={{
        isActive,
        currentStage,
        completedStages,
        status,
        scenario,
        state,
        refetch: fetchSession
      }}
    >
      {children}
    </LabSessionContext.Provider>
  )
}

export const useLabSession = () => {
  const context = useContext(LabSessionContext)
  if (!context) {
    throw new Error('useLabSession must be used within a LabSessionProvider')
  }
  return context
}
