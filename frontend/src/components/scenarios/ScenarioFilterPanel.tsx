interface ScenarioFilterPanelProps {
  categories: string[]
  difficulties: string[]
  selectedCategory: string
  selectedDifficulty: string
  selectedStatus: string
  onCategoryChange: (c: string) => void
  onDifficultyChange: (d: string) => void
  onStatusChange: (s: string) => void
}

export function ScenarioFilterPanel({
  categories,
  difficulties,
  selectedCategory,
  selectedDifficulty,
  selectedStatus,
  onCategoryChange,
  onDifficultyChange,
  onStatusChange
}: ScenarioFilterPanelProps) {
  
  return (
    <div className="flex flex-wrap items-center gap-3">
      <select 
        value={selectedCategory} 
        onChange={(e) => onCategoryChange(e.target.value)}
        className="px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 min-w-[140px]"
      >
        <option value="">All Categories</option>
        {categories.map(c => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>

      <select 
        value={selectedDifficulty} 
        onChange={(e) => onDifficultyChange(e.target.value)}
        className="px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 min-w-[140px]"
      >
        <option value="">All Difficulties</option>
        {difficulties.map(d => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>

      <select 
        value={selectedStatus} 
        onChange={(e) => onStatusChange(e.target.value)}
        className="px-3 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 min-w-[140px]"
      >
        <option value="">All Statuses</option>
        <option value="Not Started">Not Started</option>
        <option value="In Progress">In Progress</option>
        <option value="Completed">Completed</option>
      </select>
    </div>
  )
}
