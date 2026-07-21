import { cn } from '@/lib/utils'

interface DifficultyBadgeProps {
  difficulty: string
  className?: string
}

export function DifficultyBadge({ difficulty, className }: DifficultyBadgeProps) {
  const diff = difficulty.toLowerCase()
  let colorClass = 'bg-slate-500/10 text-slate-500 border-slate-500/20'

  if (diff === 'beginner') {
    colorClass = 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20'
  } else if (diff === 'intermediate') {
    colorClass = 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20'
  } else if (diff === 'advanced') {
    colorClass = 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20'
  } else if (diff === 'expert') {
    colorClass = 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20'
  }

  return (
    <span className={cn('px-2.5 py-0.5 rounded-full text-xs font-semibold border', colorClass, className)}>
      {difficulty}
    </span>
  )
}
