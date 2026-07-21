import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { scenariosService } from '@/services/scenarios'
import { QUERY_KEYS } from '@/constants/queryKeys'
import { useState, useEffect } from 'react'


export const useScenarios = () => {
  return useQuery({
    queryKey: [QUERY_KEYS.SCENARIOS],
    queryFn: scenariosService.getScenarios
  })
}

export const useScenario = (id: string) => {
  return useQuery({
    queryKey: [QUERY_KEYS.SCENARIO, id],
    queryFn: () => scenariosService.getScenario(id),
    enabled: !!id
  })
}

export const useScenarioProgress = (id: string) => {
  return useQuery({
    queryKey: [QUERY_KEYS.SCENARIO_PROGRESS, id],
    queryFn: () => scenariosService.getScenarioProgress(id),
    enabled: !!id
  })
}

export const useLaunchScenario = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => scenariosService.launchScenario(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.SCENARIO_PROGRESS, id] })
    }
  })
}

export const useScenarioCategories = () => {
  return useQuery({
    queryKey: [QUERY_KEYS.SCENARIO_CATEGORIES],
    queryFn: scenariosService.getScenarioCategories
  })
}

// Local Storage Hook for Favorites
export const useFavorites = () => {
  const [favorites, setFavorites] = useState<string[]>([])

  useEffect(() => {
    const saved = localStorage.getItem('neofactory_scenario_favorites')
    if (saved) {
      try {
        setFavorites(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to parse favorites')
      }
    }
  }, [])

  const toggleFavorite = (id: string) => {
    setFavorites(prev => {
      const newFavs = prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id]
      localStorage.setItem('neofactory_scenario_favorites', JSON.stringify(newFavs))
      return newFavs
    })
  }

  return { favorites, toggleFavorite }
}

// Local Storage Hook for Recent Activity
export const useRecentScenarios = () => {
  const [recent, setRecent] = useState<string[]>([])

  useEffect(() => {
    const saved = localStorage.getItem('neofactory_recent_scenarios')
    if (saved) {
      try {
        setRecent(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to parse recent scenarios')
      }
    }
  }, [])

  const addRecent = (id: string) => {
    setRecent(prev => {
      const newRecent = [id, ...prev.filter(r => r !== id)].slice(0, 5) // Keep last 5
      localStorage.setItem('neofactory_recent_scenarios', JSON.stringify(newRecent))
      return newRecent
    })
  }

  return { recent, addRecent }
}
