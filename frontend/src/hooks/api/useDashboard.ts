import { useQuery } from '@tanstack/react-query'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { dashboardService } from '@/services/dashboard'

export function useDashboardSummary() {
  return useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD, 'summary'],
    queryFn: () => dashboardService.getSummary(),
    staleTime: 60 * 1000, // 1 minute
  })
}

export function useDashboardAssets() {
  return useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD, 'assets'],
    queryFn: () => dashboardService.getAssetsStats(),
    staleTime: 60 * 1000,
  })
}

export function useDashboardMaintenance() {
  return useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD, 'maintenance'],
    queryFn: () => dashboardService.getMaintenanceStats(),
    staleTime: 60 * 1000,
  })
}
