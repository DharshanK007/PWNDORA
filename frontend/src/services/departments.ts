import api from '@/lib/axios'
import type { PagedResponse } from './employees'

export interface Department {
  id: string
  name: string
  description?: string
  manager_id?: string
  location?: string
  created_at: string
}

export const departmentsService = {
  getDepartments: async (skip = 0, limit = 100): Promise<PagedResponse<Department>> => {
    const { data } = await api.get(`/departments/?skip=${skip}&limit=${limit}`)
    return data
  },
  getDepartment: async (id: string): Promise<Department> => {
    const { data } = await api.get(`/departments/${id}`)
    return data
  }
}
