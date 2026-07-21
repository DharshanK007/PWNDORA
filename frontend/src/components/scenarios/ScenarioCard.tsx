import { Shield, Clock, Heart, Play, ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'
import type { Scenario } from '@/types/scenario'
import { DifficultyBadge } from './DifficultyBadge'
import { CategoryBadge } from './CategoryBadge'
import { ScenarioProgress } from './ScenarioProgress'
import { useFavorites } from '@/hooks/api/useScenarios'

interface ScenarioCardProps {
  scenario: Scenario
}

export function ScenarioCard({ scenario }: ScenarioCardProps) {
  const { favorites, toggleFavorite } = useFavorites()
  const isFavorite = favorites.includes(scenario.id)

  return (
    <div className="group relative flex flex-col rounded-xl border border-border bg-card overflow-hidden hover:shadow-lg hover:border-primary/50 transition-all duration-300">
      {/* Header/Cover */}
      <div className="h-32 bg-muted relative p-4 flex items-start justify-between bg-gradient-to-br from-slate-800 to-slate-900">
        <div className="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]" />
        <div className="relative z-10 flex items-center gap-3">
          <div className="p-2.5 bg-background/90 rounded-lg shadow-sm border border-border/50">
            <Shield className="h-6 w-6 text-primary" />
          </div>
        </div>
        <button 
          onClick={(e) => {
            e.preventDefault()
            toggleFavorite(scenario.id)
          }}
          className="relative z-10 p-2 rounded-full hover:bg-background/20 transition-colors"
        >
          <Heart 
            className={`h-5 w-5 transition-colors ${isFavorite ? 'fill-rose-500 text-rose-500' : 'text-slate-300 hover:text-white'}`} 
          />
        </button>
      </div>

      {/* Body */}
      <div className="flex flex-col flex-1 p-5">
        <div className="flex items-center gap-2 mb-3">
          <DifficultyBadge difficulty={scenario.difficulty} />
          <CategoryBadge category={scenario.category} />
        </div>
        
        <h3 className="font-semibold text-lg text-foreground mb-2 line-clamp-1 group-hover:text-primary transition-colors">
          {scenario.title}
        </h3>
        
        <p className="text-sm text-muted-foreground line-clamp-2 mb-4 flex-1">
          {scenario.description}
        </p>

        <div className="flex items-center gap-4 text-xs text-muted-foreground font-medium mb-5">
          <div className="flex items-center gap-1.5">
            <Clock className="h-3.5 w-3.5" />
            {scenario.estimatedTime || '45 mins'}
          </div>
        </div>

        <ScenarioProgress status={scenario.status || 'Not Started'} percentage={scenario.completionPercentage} />
      </div>

      {/* Footer / Actions */}
      <div className="p-5 pt-0 mt-auto flex items-center justify-between border-t border-border/50 bg-muted/10">
        <Link 
          to={`/scenarios/${scenario.id}`}
          className="text-sm font-medium text-muted-foreground hover:text-foreground flex items-center gap-1 mt-4 transition-colors"
        >
          View Details
          <ArrowRight className="h-4 w-4" />
        </Link>
        <Link
          to={`/scenarios/${scenario.id}?launch=true`}
          className="mt-4 inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 py-2"
        >
          <Play className="h-4 w-4 fill-current" />
          Launch
        </Link>
      </div>
    </div>
  )
}
