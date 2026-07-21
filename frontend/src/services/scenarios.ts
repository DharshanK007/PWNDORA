import api from '@/lib/axios'
import type { Scenario, ScenarioState } from '@/types/scenario'

// Helper to adapt backend scenario to frontend expectations
const adaptScenario = (raw: any): Scenario => ({
  id: raw.id,
  title: raw.name || raw.title || raw.id,
  description: raw.business_context || raw.description || '',
  difficulty: raw.difficulty || 'Beginner',
  category: raw.category || 'General',
  name: raw.name,
  business_context: raw.business_context,
  required_role: raw.required_role,
  stages: raw.stages || [],
  estimatedTime: '45 mins', // Placeholder as backend doesn't provide
  tags: raw.category ? [raw.category] : [],
  author: 'NeoFactory Team',
  objectives: raw.stages?.map((s: any) => s.objective) || []
})

export const scenariosService = {
  getScenarios: async (): Promise<Scenario[]> => {
    const { data } = await api.get('/scenarios/')
    return (data || []).map(adaptScenario)
  },
  
  getScenario: async (id: string): Promise<Scenario> => {
    const { data } = await api.get(`/scenarios/${id}`)
    return adaptScenario(data)
  },

  launchScenario: async (id: string): Promise<{ status: string, state: ScenarioState }> => {
    const { data } = await api.post(`/scenarios/${id}/start`)
    return data
  },

  getScenarioProgress: async (id: string): Promise<ScenarioState | null> => {
    try {
      const { data } = await api.get(`/scenarios/${id}/state`)
      return data
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null // Not Started
      }
      throw error
    }
  },

  getScenarioCategories: async (): Promise<string[]> => {
    const { data } = await api.get('/scenarios/')
    const categories = new Set<string>()
    data.forEach((s: any) => {
      if (s.category) categories.add(s.category)
    })
    return Array.from(categories)
  },

  getScenarioDifficulties: async (): Promise<string[]> => {
    const { data } = await api.get('/scenarios/')
    const difficulties = new Set<string>()
    data.forEach((s: any) => {
      if (s.difficulty) difficulties.add(s.difficulty)
    })
    return Array.from(difficulties)
  }
}
