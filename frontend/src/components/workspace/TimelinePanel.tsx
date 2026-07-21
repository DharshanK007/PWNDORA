import { Clock, Info, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react'
import type { TimelineEvent } from '@/types/workspace'

interface TimelinePanelProps {
  events: TimelineEvent[]
}

export function TimelinePanel({ events }: TimelinePanelProps) {
  const getIcon = (type: TimelineEvent['type']) => {
    switch (type) {
      case 'SUCCESS': return <CheckCircle2 className="w-4 h-4 text-emerald-500" />
      case 'WARNING': return <AlertTriangle className="w-4 h-4 text-orange-500" />
      case 'ERROR': return <XCircle className="w-4 h-4 text-red-500" />
      case 'INFO':
      default: return <Info className="w-4 h-4 text-blue-500" />
    }
  }

  return (
    <div className="flex flex-col h-full bg-slate-900 border-l border-slate-800">
      <div className="p-3 border-b border-slate-800 flex items-center">
        <Clock className="w-4 h-4 mr-2 text-blue-400" />
        <h2 className="text-sm font-semibold text-slate-200">Timeline</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {events.length === 0 ? (
          <div className="text-center py-8 text-slate-500 text-sm">
            No events recorded yet.
          </div>
        ) : (
          <div className="relative">
            {/* Connecting vertical line */}
            <div className="absolute left-3 top-2 bottom-2 w-px bg-slate-800" />
            
            <div className="space-y-4">
              {events.map((event) => (
                <div key={event.id} className="relative pl-8 flex items-start group">
                  <div className="absolute left-1 top-0.5 bg-slate-900 p-1 rounded-full z-10 border border-slate-800 group-hover:border-slate-700 transition-colors">
                    {getIcon(event.type)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-baseline justify-between mb-0.5">
                      <span className="text-sm font-medium text-slate-200">
                        {event.message}
                      </span>
                      <span className="text-[10px] text-slate-500 ml-2 whitespace-nowrap">
                        {new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
