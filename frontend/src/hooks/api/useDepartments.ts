import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { departmentsService } from '@/services/departments'

export function useDepartments(skip = 0, limit = 100) {
  return useQuery({
    queryKey: [QUERY_KEYS.DEPARTMENTS, { skip, limit }],
    queryFn: () => departmentsService.getDepartments(skip, limit),
    staleTime: 5 * 60 * 1000,
  })
}

export function useDepartment(id: string) {
  return useQuery({
    queryKey: [QUERY_KEYS.DEPARTMENT, id],
    queryFn: () => departmentsService.getDepartment(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}
