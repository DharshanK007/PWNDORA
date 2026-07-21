import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { usersService } from '@/services/users'

export function useUsers(skip = 0, limit = 100) {
  return useQuery({
    queryKey: [QUERY_KEYS.USERS, { skip, limit }],
    queryFn: () => usersService.getUsers(skip, limit),
    staleTime: 5 * 60 * 1000,
  })
}

export function useUser(id: string) {
  return useQuery({
    queryKey: [QUERY_KEYS.USER, id],
    queryFn: () => usersService.getUser(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}
