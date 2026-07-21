import api from '@/lib/axios'

export interface Employee {
  id: string
  first_name: string
  last_name: string
  phone?: string
  title?: string
  department_id: string | null
  status: string
  clearance_level: number
  hire_date?: string
}

export interface PagedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export const employeesService = {
  getEmployees: async (skip = 0, limit = 100): Promise<PagedResponse<Employee>> => {
    const { data } = await api.get(`/employees/?skip=${skip}&limit=${limit}`)
    return data
  },
  getEmployee: async (id: string): Promise<Employee> => {
    const { data } = await api.get(`/employees/${id}`)
    return data
  }
}
