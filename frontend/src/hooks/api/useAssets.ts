import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { assetsService } from '@/services/assets'

export function useAssets(skip = 0, limit = 100) {
  return useQuery({
    queryKey: [QUERY_KEYS.ASSETS, { skip, limit }],
    queryFn: () => assetsService.getAssets(skip, limit),
    staleTime: 5 * 60 * 1000,
  })
}

export function useAsset(id: string) {
  return useQuery({
    queryKey: [QUERY_KEYS.ASSET, id],
    queryFn: () => assetsService.getAsset(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}
