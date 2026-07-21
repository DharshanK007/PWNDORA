import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { maintenanceService } from '@/services/maintenance'

export function useTickets(skip = 0, limit = 100) {
  return useQuery({
    queryKey: [QUERY_KEYS.MAINTENANCE, { skip, limit }],
    queryFn: () => maintenanceService.getTickets(skip, limit),
    staleTime: 5 * 60 * 1000,
  })
}

export function useTicket(id: string) {
  return useQuery({
    queryKey: [QUERY_KEYS.TICKET, id],
    queryFn: () => maintenanceService.getTicket(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}
