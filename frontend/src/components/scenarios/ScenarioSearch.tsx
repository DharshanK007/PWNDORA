import { Search } from 'lucide-react'

interface ScenarioSearchProps {
  value: string
  onChange: (value: string) => void
}

export function ScenarioSearch({ value, onChange }: ScenarioSearchProps) {
  return (
    <div className="relative flex-1">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <input
        type="text"
        placeholder="Search scenarios by title, description, or tags... (Ctrl+K)"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full pl-9 pr-4 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-shadow"
      />
    </div>
  )
}
