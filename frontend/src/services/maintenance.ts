import api from '@/lib/axios'
import type { PagedResponse } from './employees'

export interface MaintenanceTicket {
  id: string
  title: string
  description?: string
  status: string
  priority: string
  device_id?: string
  assigned_to?: string
  created_at: string
  updated_at: string
}

export const maintenanceService = {
  getTickets: async (skip = 0, limit = 100): Promise<PagedResponse<MaintenanceTicket>> => {
    const { data } = await api.get(`/tickets/?skip=${skip}&limit=${limit}`)
    return data
  },
  getTicket: async (id: string): Promise<MaintenanceTicket> => {
    const { data } = await api.get(`/tickets/${id}`)
    return data
  }
}
