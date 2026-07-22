import api from '@/lib/axios'
import type { PagedResponse } from './employees'

export interface Report {
  id: string
  title: string
  type: string
  status: string
  summary?: string
  generated_by?: string
  created_at: string
}

export const reportsService = {
  getReports: async (skip = 0, limit = 100): Promise<PagedResponse<Report>> => {
    const { data } = await api.get(`/reports/?skip=${skip}&limit=${limit}`)
    return data
  },
  getReport: async (id: string): Promise<Report> => {
    const { data } = await api.get(`/reports/${id}`)
    return data
  }
}
