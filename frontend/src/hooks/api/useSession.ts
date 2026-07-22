import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { sessionService } from '@/services/session'
import { QUERY_KEYS } from '@/constants/queryKeys'
import type { WorkspaceState } from '@/types/workspace'
import { useState, useEffect } from 'react'

export const useCurrentSession = (scenarioId: string) => {
  return useQuery({
    queryKey: [QUERY_KEYS.SCENARIOS, scenarioId, 'session'],
    queryFn: () => sessionService.getSessionState(scenarioId),
    enabled: !!scenarioId,
    retry: false, // Don't retry if state not found (user hasn't started it yet)
  })
}

export const useStartSession = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (scenarioId: string) => sessionService.startSession(scenarioId),
    onSuccess: (data, scenarioId) => {
      queryClient.setQueryData([QUERY_KEYS.SCENARIOS, scenarioId, 'session'], data)
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.SCENARIOS, scenarioId, 'progress'] })
    }
  })
}

export const useEndSession = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (scenarioId: string) => sessionService.resetSession(scenarioId),
    onSuccess: (_, scenarioId) => {
      // Clear session from react-query cache
      queryClient.removeQueries({ queryKey: [QUERY_KEYS.SCENARIOS, scenarioId, 'session'] })
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.SCENARIOS, scenarioId, 'progress'] })
      // Clear workspace local storage
      localStorage.removeItem(`neofactory_workspace_${scenarioId}`)
    }
  })
}

export const usePerformAction = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ scenarioId, action }: { scenarioId: string, action: string }) => 
      sessionService.performAction(scenarioId, action),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.SCENARIOS, variables.scenarioId, 'session'] })
    }
  })
}

const DEFAULT_WORKSPACE: Omit<WorkspaceState, 'scenarioId'> = {
  layout: {
    sizes: { left: 25, right: 25, bottom: 30 },
    collapsed: { left: false, right: false, bottom: false }
  },
  openFiles: [],
  selectedEvidenceId: null,
  notes: '# Investigation Notes\n\nStart typing here...',
  timeline: []
}

export const useWorkspace = (scenarioId: string) => {
  const storageKey = `neofactory_workspace_${scenarioId}`
  
  // Initialize from local storage or default
  const [workspace, setWorkspace] = useState<WorkspaceState>(() => {
    try {
      const stored = localStorage.getItem(storageKey)
      if (stored) {
        return { ...DEFAULT_WORKSPACE, ...JSON.parse(stored), scenarioId }
      }
    } catch (e) {
      console.error('Failed to parse workspace state from local storage', e)
    }
    return { ...DEFAULT_WORKSPACE, scenarioId }
  })

  // Sync to local storage whenever workspace changes
  useEffect(() => {
    if (scenarioId && workspace) {
      localStorage.setItem(storageKey, JSON.stringify(workspace))
    }
  }, [scenarioId, workspace, storageKey])

  const updateWorkspace = (updates: Partial<WorkspaceState>) => {
    setWorkspace(prev => ({ ...prev, ...updates }))
  }

  const updateLayout = (updates: Partial<WorkspaceState['layout']>) => {
    setWorkspace(prev => ({
      ...prev,
      layout: { ...prev.layout, ...updates }
    }))
  }

  const addTimelineEvent = (event: Omit<WorkspaceState['timeline'][0], 'id' | 'timestamp'>) => {
    const newEvent = {
      ...event,
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString()
    }
    setWorkspace(prev => ({
      ...prev,
      timeline: [...prev.timeline, newEvent]
    }))
  }

  return {
    workspace,
    updateWorkspace,
    updateLayout,
    addTimelineEvent,
    resetWorkspace: () => {
      setWorkspace({ ...DEFAULT_WORKSPACE, scenarioId })
    }
  }
}
