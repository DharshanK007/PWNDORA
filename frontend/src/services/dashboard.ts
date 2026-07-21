import api from '@/lib/axios'

export interface DashboardSummary {
  assets: { total: number; online: number }
  employees: { total: number; active: number }
  tickets: { total: number; open: number }
}

export const dashboardService = {
  getSummary: async (): Promise<DashboardSummary> => {
    const { data } = await api.get('/dashboard/summary')
    return data
  },
  getAssetsStats: async () => {
    const { data } = await api.get('/dashboard/assets')
    return data
  },
  getMaintenanceStats: async () => {
    const { data } = await api.get('/dashboard/maintenance')
    return data
  },
}
