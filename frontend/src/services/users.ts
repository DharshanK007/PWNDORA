import api from '@/lib/axios'
import type { PagedResponse } from './employees'

export interface User {
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean
  role: string
  created_at: string
}

export const usersService = {
  getUsers: async (skip = 0, limit = 100): Promise<PagedResponse<User>> => {
    const { data } = await api.get(`/users/?skip=${skip}&limit=${limit}`)
    return data
  },
  getUser: async (id: string): Promise<User> => {
    const { data } = await api.get(`/users/${id}`)
    return data
  }
}
