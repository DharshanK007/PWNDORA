import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { reportsService } from '@/services/reports'

export function useReports(skip = 0, limit = 100) {
  return useQuery({
    queryKey: [QUERY_KEYS.REPORTS, { skip, limit }],
    queryFn: () => reportsService.getReports(skip, limit),
    staleTime: 5 * 60 * 1000,
  })
}

export function useReport(id: string) {
  return useQuery({
    queryKey: [QUERY_KEYS.REPORT, id],
    queryFn: () => reportsService.getReport(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}
