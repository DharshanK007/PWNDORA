import { Terminal, Search, Filter } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'

interface LogEntry {
  id: string
  timestamp: string
  level: 'INFO' | 'WARN' | 'ERROR' | 'DEBUG'
  source: string
  message: string
}

interface LogViewerProps {
  logs: LogEntry[]
}

export function LogViewer({ logs }: LogViewerProps) {
  const [search, setSearch] = useState('')
  const [levelFilter, setLevelFilter] = useState<string>('ALL')
  const bottomRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom on new logs
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs.length])

  const filteredLogs = logs.filter(log => {
    if (levelFilter !== 'ALL' && log.level !== levelFilter) return false
    if (search && !log.message.toLowerCase().includes(search.toLowerCase()) && 
        !log.source.toLowerCase().includes(search.toLowerCase())) {
      return false
    }
    return true
  })

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'ERROR': return 'text-red-400 bg-red-400/10'
      case 'WARN': return 'text-orange-400 bg-orange-400/10'
      case 'DEBUG': return 'text-slate-400 bg-slate-800'
      case 'INFO':
      default: return 'text-blue-400 bg-blue-500/10'
    }
  }

  return (
    <div className="flex flex-col h-full bg-[#0a0a0a] border-t border-slate-800">
      <div className="bg-slate-900 border-b border-slate-800 px-4 py-2 flex items-center justify-between shrink-0">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center">
          <Terminal className="w-4 h-4 mr-2 text-emerald-500" />
          Terminal Logs
        </h3>
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2 top-2 text-slate-500" />
            <input
              type="text"
              placeholder="Filter logs..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-slate-950 border border-slate-700 text-xs rounded pl-7 pr-2 py-1.5 text-slate-300 placeholder-slate-500 focus:outline-none focus:border-blue-500 w-48"
            />
          </div>
          <div className="flex items-center space-x-2 bg-slate-950 border border-slate-700 rounded px-2 py-1">
            <Filter className="w-3 h-3 text-slate-500" />
            <select 
              className="bg-transparent text-xs text-slate-300 focus:outline-none appearance-none cursor-pointer"
              value={levelFilter}
              onChange={(e) => setLevelFilter(e.target.value)}
            >
              <option value="ALL">All Levels</option>
              <option value="ERROR">Errors</option>
              <option value="WARN">Warnings</option>
              <option value="INFO">Info</option>
            </select>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4 font-mono text-[11px] leading-relaxed">
        {filteredLogs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-600">
            <Terminal className="w-8 h-8 mb-2 opacity-50" />
            <p>No logs available or matching filter.</p>
          </div>
        ) : (
          <div className="space-y-1">
            {filteredLogs.map(log => (
              <div key={log.id} className="flex items-start hover:bg-slate-800/30 px-2 py-1 -mx-2 rounded transition-colors group">
                <span className="text-slate-500 w-24 shrink-0">{new Date(log.timestamp).toLocaleTimeString([], { hour12: false })}</span>
                <span className={`w-16 shrink-0 px-1.5 rounded-sm text-[9px] font-bold tracking-wider text-center ${getLevelColor(log.level)} mr-3`}>
                  {log.level}
                </span>
                <span className="text-slate-400 w-32 shrink-0 truncate mr-3" title={log.source}>
                  [{log.source}]
                </span>
                <span className={`flex-1 break-all ${log.level === 'ERROR' ? 'text-red-300' : 'text-slate-300'}`}>
                  {log.message}
                </span>
              </div>
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>
    </div>
  )
}
