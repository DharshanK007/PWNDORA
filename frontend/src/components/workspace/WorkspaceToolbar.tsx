import { ArrowLeft, Save, LayoutGrid, Maximize, Power } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useEndSession } from '@/hooks/api/useSession'
import { useNavigate } from 'react-router-dom'

interface WorkspaceToolbarProps {
  scenarioId: string
  onResetLayout: () => void
  onSaveNotes?: () => void
}

export function WorkspaceToolbar({ scenarioId, onResetLayout, onSaveNotes }: WorkspaceToolbarProps) {
  const endSession = useEndSession()
  const navigate = useNavigate()

  const handleEndSession = async () => {
    if (confirm('Are you sure you want to end this session? All progress and notes will be permanently reset.')) {
      await endSession.mutateAsync(scenarioId)
      navigate('/scenarios')
    }
  }

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`)
      })
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen()
      }
    }
  }

  return (
    <div className="bg-slate-800 border-b border-slate-700 px-4 py-2 flex items-center justify-between text-sm">
      <div className="flex items-center space-x-2">
        <Link 
          to="/scenarios"
          className="flex items-center px-3 py-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Catalog
        </Link>
      </div>

      <div className="flex items-center space-x-2">
        {onSaveNotes && (
          <button 
            onClick={onSaveNotes}
            className="flex items-center px-3 py-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
            title="Force save notes"
          >
            <Save className="w-4 h-4 mr-2" />
            Save Notes
          </button>
        )}
        
        <button 
          onClick={onResetLayout}
          className="flex items-center px-3 py-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
        >
          <LayoutGrid className="w-4 h-4 mr-2" />
          Reset Layout
        </button>
        
        <div className="w-px h-5 bg-slate-600 mx-2" />

        <button 
          onClick={toggleFullscreen}
          className="flex items-center p-1.5 text-slate-400 hover:text-white hover:bg-slate-700 rounded transition-colors"
          title="Toggle Fullscreen"
        >
          <Maximize className="w-4 h-4" />
        </button>

        <button 
          onClick={handleEndSession}
          disabled={endSession.isPending}
          className="flex items-center px-3 py-1.5 text-red-400 hover:text-red-300 hover:bg-red-400/10 rounded transition-colors font-medium ml-2"
        >
          <Power className="w-4 h-4 mr-2" />
          {endSession.isPending ? 'Ending...' : 'End Session'}
        </button>
      </div>
    </div>
  )
}
