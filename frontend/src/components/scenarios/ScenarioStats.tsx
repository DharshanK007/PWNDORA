import { Target, Clock, ShieldCheck, Star } from 'lucide-react'

interface ScenarioStatsProps {
  total: number
  inProgress: number
  completed: number
  recommended: number
}

export function ScenarioStats({ total, inProgress, completed, recommended }: ScenarioStatsProps) {
  const stats = [
    { label: 'Available Scenarios', value: total, icon: Target, color: 'text-blue-500', bg: 'bg-blue-500/10' },
    { label: 'In Progress', value: inProgress, icon: Clock, color: 'text-amber-500', bg: 'bg-amber-500/10' },
    { label: 'Completed', value: completed, icon: ShieldCheck, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
    { label: 'Recommended', value: recommended, icon: Star, color: 'text-purple-500', bg: 'bg-purple-500/10' },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((stat, i) => (
        <div key={i} className="flex items-center gap-4 p-4 rounded-xl border border-border bg-card">
          <div className={`p-3 rounded-lg ${stat.bg}`}>
            <stat.icon className={`h-6 w-6 ${stat.color}`} />
          </div>
          <div>
            <div className="text-2xl font-bold text-foreground">{stat.value}</div>
            <div className="text-xs font-medium text-muted-foreground">{stat.label}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
