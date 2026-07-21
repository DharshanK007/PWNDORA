import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { employeesService } from '@/services/employees'

export function useEmployees(skip = 0, limit = 100) {
  return useQuery({
    queryKey: [QUERY_KEYS.EMPLOYEES, { skip, limit }],
    queryFn: () => employeesService.getEmployees(skip, limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useEmployee(id: string) {
  return useQuery({
    queryKey: [QUERY_KEYS.EMPLOYEE, id],
    queryFn: () => employeesService.getEmployee(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}
