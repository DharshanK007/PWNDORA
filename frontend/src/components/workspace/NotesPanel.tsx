import { Edit3, Copy, Trash2, CheckCircle2 } from 'lucide-react'
import { useState, useEffect } from 'react'

interface NotesPanelProps {
  initialNotes: string
  onChange: (notes: string) => void
}

export function NotesPanel({ initialNotes, onChange }: NotesPanelProps) {
  const [notes, setNotes] = useState(initialNotes)
  const [copied, setCopied] = useState(false)

  // Sync internal state if initialNotes changes from outside (e.g., reset layout)
  useEffect(() => {
    setNotes(initialNotes)
  }, [initialNotes])

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setNotes(e.target.value)
    onChange(e.target.value)
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(notes)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleClear = () => {
    if (confirm('Are you sure you want to clear your notes?')) {
      setNotes('')
      onChange('')
    }
  }

  return (
    <div className="flex flex-col h-full bg-slate-900 border-r border-slate-800">
      <div className="p-3 border-b border-slate-800 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center">
          <Edit3 className="w-4 h-4 mr-2 text-blue-400" />
          Investigation Notes
        </h2>
        <div className="flex items-center space-x-1">
          <button 
            onClick={handleCopy}
            className="p-1 text-slate-400 hover:text-white hover:bg-slate-800 rounded transition-colors"
            title="Copy all notes"
          >
            {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
          </button>
          <button 
            onClick={handleClear}
            className="p-1 text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded transition-colors"
            title="Clear notes"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      <div className="flex-1 p-0 relative">
        <textarea
          value={notes}
          onChange={handleChange}
          placeholder="Start typing your investigation notes here. Supports Markdown format. Autosaves locally."
          className="w-full h-full bg-transparent text-slate-300 text-sm p-4 resize-none focus:outline-none focus:ring-inset focus:ring-1 focus:ring-blue-500/50 leading-relaxed font-mono"
        />
        <div className="absolute bottom-2 right-4 text-[10px] text-slate-500 uppercase font-semibold">
          Autosaving...
        </div>
      </div>
    </div>
  )
}
