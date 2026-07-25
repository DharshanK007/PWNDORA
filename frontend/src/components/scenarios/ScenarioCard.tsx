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
    <div className="group relative flex flex-col md:flex-row w-full rounded-2xl border border-border bg-card overflow-hidden hover:shadow-xl hover:border-primary/40 transition-all duration-300">
      {/* Left Portion: Details & Information */}
      <div className="flex flex-col flex-1 p-6 md:p-8 md:w-[60%]">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <DifficultyBadge difficulty={scenario.difficulty} />
            <CategoryBadge category={scenario.category} />
          </div>
          <button 
            onClick={(e) => {
              e.preventDefault()
              toggleFavorite(scenario.id)
            }}
            className="p-2 rounded-full hover:bg-muted transition-colors"
          >
            <Heart 
              className={`h-5 w-5 transition-colors ${isFavorite ? 'fill-rose-500 text-rose-500' : 'text-muted-foreground hover:text-foreground'}`} 
            />
          </button>
        </div>
        
        <h3 className="font-bold text-2xl text-foreground mb-3 group-hover:text-primary transition-colors">
          {scenario.title}
        </h3>
        
        <p className="text-base text-muted-foreground mb-6 leading-relaxed flex-1">
          {scenario.description}
        </p>

        <div className="flex items-center gap-6 text-sm text-muted-foreground font-medium mb-6">
          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4" />
            {scenario.estimatedTime || '45 mins'}
          </div>
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4" />
            Cyber Range Lab
          </div>
        </div>

        <div className="mb-6 max-w-md">
          <ScenarioProgress status={scenario.status || 'Not Started'} percentage={scenario.completionPercentage} />
        </div>

        {/* Footer Actions */}
        <div className="flex items-center gap-4 mt-auto">
          <Link
            to={`/scenarios/${scenario.id}?launch=true`}
            className="inline-flex items-center justify-center gap-2 rounded-lg text-sm font-semibold ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-6"
          >
            <Play className="h-4 w-4 fill-current" />
            Launch Lab
          </Link>
          <Link 
            to={`/scenarios/${scenario.id}`}
            className="inline-flex items-center justify-center gap-2 rounded-lg text-sm font-semibold transition-colors bg-secondary text-secondary-foreground hover:bg-secondary/80 h-10 px-6"
          >
            View Details
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>

      {/* Right Portion: Generative Cybersecurity Image */}
      <div className="md:w-[40%] min-h-[250px] relative overflow-hidden bg-muted/20 border-t md:border-t-0 md:border-l border-border">
        {/* Generative Asset Logic */}
        <img 
          src={`/images/scenarios/${scenario.id}.png`} 
          alt={scenario.title}
          className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-in-out"
          onError={(e) => {
            // Fallback if image doesn't exist (e.g. for new scenarios)
            (e.target as HTMLImageElement).src = 'https://www.transparenttextures.com/patterns/carbon-fibre.png';
            (e.target as HTMLImageElement).className = "absolute inset-0 w-full h-full object-cover opacity-20 bg-slate-900";
          }}
        />
        {/* Subtle gradient overlay to blend into the card */}
        <div className="absolute inset-0 bg-gradient-to-r from-card to-transparent w-24 hidden md:block" />
        <div className="absolute inset-0 bg-gradient-to-t from-card to-transparent h-24 mt-auto md:hidden" />
      </div>
    </div>
  )
}
