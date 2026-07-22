import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { scenariosService } from '@/services/scenarios'
import type { ScenarioState, Scenario } from '@/types/scenario'
import { useAuth } from '@/hooks/useAuth'

interface LabSessionContextType {
  isActive: boolean
  currentStage: number
  completedStages: (string | number)[]
  status: 'IN_PROGRESS' | 'COMPLETED' | 'NOT_STARTED' | string
  scenario: Scenario | null
  state: ScenarioState | null
  refetch: () => Promise<void>
}

const LabSessionContext = createContext<LabSessionContextType | undefined>(undefined)

export const PILOT_SCENARIO_ID = 'operation_phantom_firmware'

export const LabSessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth()
  const [state, setState] = useState<ScenarioState | null>(null)
  const [scenario, setScenario] = useState<Scenario | null>(null)

  const fetchSession = useCallback(async () => {
    if (!isAuthenticated) return
    try {
      const [prog, scen] = await Promise.all([
        scenariosService.getScenarioProgress(PILOT_SCENARIO_ID),
        scenariosService.getScenario(PILOT_SCENARIO_ID).catch(() => null)
      ])
      setState(prog)
      if (scen) setScenario(scen)
    } catch (e) {
      // Ignore polling errors silently
    }
  }, [isAuthenticated])

  useEffect(() => {
    if (isAuthenticated) {
      fetchSession()
      const interval = setInterval(fetchSession, 3000)
      return () => clearInterval(interval)
    } else {
      setState(null)
      setScenario(null)
    }
  }, [isAuthenticated, fetchSession])

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
