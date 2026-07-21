import api from '@/lib/axios'
import type { SessionStateResponse } from '@/types/session'

export const sessionService = {
  startSession: async (scenarioId: string): Promise<SessionStateResponse> => {
    const { data } = await api.post(`/scenarios/${scenarioId}/start`)
    return data.state
  },
  
  resetSession: async (scenarioId: string): Promise<void> => {
    await api.post(`/scenarios/${scenarioId}/reset`)
  },
  
  getSessionState: async (scenarioId: string): Promise<SessionStateResponse> => {
    const { data } = await api.get(`/scenarios/${scenarioId}/state`)
    return data
  }
}
