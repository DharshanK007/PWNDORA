import { FileText, Image as ImageIcon, FileJson, AlignLeft, ShieldAlert, Cpu } from 'lucide-react'
import type { Evidence } from '@/types/workspace'

interface EvidenceCardProps {
  evidence: Evidence
  isSelected: boolean
  onClick: () => void
}

export function EvidenceCard({ evidence, isSelected, onClick }: EvidenceCardProps) {
  const getIcon = () => {
    switch (evidence.type) {
      case 'log': return <AlignLeft className="w-5 h-5 text-emerald-400" />
      case 'json': return <FileJson className="w-5 h-5 text-yellow-400" />
      case 'yaml': return <FileText className="w-5 h-5 text-purple-400" />
      case 'image': return <ImageIcon className="w-5 h-5 text-blue-400" />
      case 'pcap': return <ShieldAlert className="w-5 h-5 text-red-400" />
      case 'memory': return <Cpu className="w-5 h-5 text-orange-400" />
      default: return <FileText className="w-5 h-5 text-slate-400" />
    }
  }

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <div 
      onClick={onClick}
      className={`
        p-3 rounded border cursor-pointer transition-colors flex items-start space-x-3
        ${isSelected 
          ? 'bg-blue-500/10 border-blue-500/50' 
          : 'bg-slate-800/50 border-slate-700 hover:bg-slate-800 hover:border-slate-600'}
      `}
    >
      <div className="p-2 bg-slate-900 rounded-lg shrink-0">
        {getIcon()}
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center justify-between mb-1">
          <h4 className={`text-sm font-medium truncate ${isSelected ? 'text-white' : 'text-slate-200'}`}>
            {evidence.name}
          </h4>
          <span className="text-[10px] text-slate-500 uppercase ml-2 shrink-0">
            {evidence.type}
          </span>
        </div>
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span className="truncate">{evidence.source}</span>
          <span className="shrink-0 ml-2">{formatSize(evidence.size)}</span>
        </div>
      </div>
    </div>
  )
}
