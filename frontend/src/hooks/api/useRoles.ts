import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { rolesService } from '@/services/roles'

export function useRoles() {
  return useQuery({
    queryKey: [QUERY_KEYS.ROLES],
    queryFn: () => rolesService.getRoles(),
    staleTime: 5 * 60 * 1000,
  })
}
