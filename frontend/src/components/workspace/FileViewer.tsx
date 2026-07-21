import { Download, Copy, Maximize2 } from 'lucide-react'
import type { Evidence } from '@/types/workspace'

interface FileViewerProps {
  file: Evidence | null
}

export function FileViewer({ file }: FileViewerProps) {
  if (!file) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-500 bg-slate-950">
        <div className="w-16 h-16 border-2 border-dashed border-slate-700 rounded-lg mb-4 flex items-center justify-center">
          <Maximize2 className="w-6 h-6 text-slate-600" />
        </div>
        <p className="font-medium">No Evidence Selected</p>
        <p className="text-sm mt-1">Select an item from the Evidence Explorer to view it here.</p>
      </div>
    )
  }

  const handleCopy = () => {
    if (file.content) {
      navigator.clipboard.writeText(file.content)
    }
  }

  // Very basic syntax highlighting simulation
  const getLanguageClass = () => {
    switch (file.type) {
      case 'json': return 'text-yellow-300'
      case 'yaml': return 'text-purple-300'
      case 'log': return 'text-emerald-300'
      default: return 'text-slate-300'
    }
  }

  return (
    <div className="flex flex-col h-full bg-slate-950">
      <div className="bg-slate-900 border-b border-slate-800 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <h3 className="text-sm font-medium text-slate-200 font-mono">{file.name}</h3>
          <span className="text-[10px] uppercase tracking-wider text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
            {file.type}
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          <button 
            onClick={handleCopy}
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded transition-colors"
            title="Copy Content"
          >
            <Copy className="w-4 h-4" />
          </button>
          <button 
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded transition-colors"
            title="Download"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4">
        {['pcap', 'memory', 'image'].includes(file.type) ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-500">
            <p>Binary format not supported in web viewer.</p>
            <button className="mt-4 flex items-center px-4 py-2 bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 rounded-md transition-colors border border-blue-500/30">
              <Download className="w-4 h-4 mr-2" />
              Download {file.name}
            </button>
          </div>
        ) : (
          <pre className={`font-mono text-xs leading-relaxed whitespace-pre-wrap ${getLanguageClass()}`}>
            {file.content || 'No content available.'}
          </pre>
        )}
      </div>
    </div>
  )
}
