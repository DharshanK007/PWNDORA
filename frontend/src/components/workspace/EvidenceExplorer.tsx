import { Search, FolderOpen, Filter } from 'lucide-react'
import type { Evidence } from '@/types/workspace'
import { EvidenceCard } from './EvidenceCard'
import { useState } from 'react'

interface EvidenceExplorerProps {
  evidence: Evidence[]
  selectedId: string | null
  onSelect: (id: string) => void
}

export function EvidenceExplorer({ evidence, selectedId, onSelect }: EvidenceExplorerProps) {
  const [search, setSearch] = useState('')

  const filtered = evidence.filter(e => 
    e.name.toLowerCase().includes(search.toLowerCase()) || 
    e.type.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="flex flex-col h-full bg-slate-900 border-r border-slate-800">
      <div className="p-3 border-b border-slate-800 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center">
          <FolderOpen className="w-4 h-4 mr-2 text-blue-400" />
          Evidence Explorer
        </h2>
        <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
          {filtered.length} Items
        </span>
      </div>

      <div className="p-3 border-b border-slate-800 space-y-3">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search evidence..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 text-sm rounded-md pl-9 pr-3 py-2 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
          />
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <Filter className="w-3 h-3 text-slate-500" />
          <span className="text-slate-500">Filter by type:</span>
          {/* We could add type filters here later */}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {filtered.length === 0 ? (
          <div className="text-center py-8 text-slate-500 text-sm">
            No evidence matches your search.
          </div>
        ) : (
          filtered.map(item => (
            <EvidenceCard
              key={item.id}
              evidence={item}
              isSelected={selectedId === item.id}
              onClick={() => onSelect(item.id)}
            />
          ))
        )}
      </div>
    </div>
  )
}
