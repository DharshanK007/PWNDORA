import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Clock, Target, Play, CheckCircle2 } from 'lucide-react'
import { Link } from 'react-router-dom'
import { PageHeader } from '@/components/common/PageHeader'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { DifficultyBadge } from '@/components/scenarios/DifficultyBadge'
import { CategoryBadge } from '@/components/scenarios/CategoryBadge'
import { useScenario, useScenarioProgress, useLaunchScenario, useRecentScenarios } from '@/hooks/api/useScenarios'

export function ScenarioDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { data: scenario, isLoading: isScenarioLoading, isError: isScenarioError } = useScenario(id!)
  const { data: progress, isLoading: isProgressLoading } = useScenarioProgress(id!)
  const { mutate: launchScenario, isPending: isLaunching } = useLaunchScenario()
  
  const { addRecent } = useRecentScenarios()
  
  const [showLaunchDialog, setShowLaunchDialog] = useState(false)

  // Track as recently viewed if we successfully loaded the scenario
  useEffect(() => {
    if (scenario) {
      addRecent(scenario.id)
    }
  }, [scenario, addRecent])

  if (isScenarioLoading || isProgressLoading) {
    return (
      <div className="flex-1 p-8">
        <div className="flex items-center justify-center h-[60vh]">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    )
  }

  if (isScenarioError || !scenario) {
    return (
      <div className="flex-1 p-8">
        <PageHeader title="Scenario Details" />
        <div className="mt-8 rounded-xl border border-destructive/50 bg-destructive/10 p-6 text-destructive">
          Failed to load scenario details. The scenario may not exist.
        </div>
      </div>
    )
  }

  const handleLaunch = () => {
    launchScenario(scenario.id, {
      onSuccess: () => {
        setShowLaunchDialog(false)
        navigate(`/investigation?scenarioId=${scenario.id}`)
      },
      onError: (err) => {
        console.error('Failed to launch scenario:', err)
        alert('Failed to launch scenario. Please try again.')
      }
    })
  }

  const status = progress ? progress.status : 'Not Started'
  const isCompleted = status === 'COMPLETED'
  const isInProgress = status === 'IN_PROGRESS'

  return (
    <div className="flex-1 p-4 md:p-8 space-y-8 animate-fade-in relative">
      <Link to="/scenarios" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors mb-2">
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Catalog
      </Link>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="xl:col-span-2 space-y-8">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <DifficultyBadge difficulty={scenario.difficulty} />
              <CategoryBadge category={scenario.category} />
            </div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground">{scenario.title}</h1>
            <p className="text-lg text-muted-foreground">{scenario.description}</p>
          </div>

          <div className="p-6 rounded-xl border border-border bg-card space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <Target className="h-5 w-5 text-primary" />
                Scenario Objectives
              </h3>
              <ul className="space-y-3">
                {scenario.objectives?.map((obj, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <div className="mt-0.5 rounded-full bg-primary/10 p-1">
                      <CheckCircle2 className="h-3.5 w-3.5 text-primary" />
                    </div>
                    <span className="text-muted-foreground">{obj}</span>
                  </li>
                ))}
                {(!scenario.objectives || scenario.objectives.length === 0) && (
                  <li className="text-muted-foreground italic">No specific objectives defined.</li>
                )}
              </ul>
            </div>
          </div>

          {/* Stages Breakdown (Read Only representation) */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Implementation Stages</h3>
            <div className="space-y-3">
              {scenario.stages?.map((stage, i) => (
                <div key={stage.id} className="p-4 rounded-lg border border-border bg-card/50 flex items-start gap-4">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-muted font-semibold text-sm">
                    {i + 1}
                  </div>
                  <div>
                    <h4 className="font-medium">{stage.objective}</h4>
                    <p className="text-sm text-muted-foreground font-mono mt-1">{stage.required_action}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <div className="p-6 rounded-xl border border-border bg-card space-y-6 sticky top-24">
            <div>
              <h3 className="font-semibold text-foreground mb-4">Scenario Details</h3>
              <div className="space-y-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Estimated Time</span>
                  <span className="font-medium flex items-center gap-1.5"><Clock className="h-3.5 w-3.5" />{scenario.estimatedTime}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Required Role</span>
                  <span className="font-medium">{scenario.required_role || 'General'}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Status</span>
                  <span className="font-medium">{isInProgress ? 'In Progress' : isCompleted ? 'Completed' : 'Not Started'}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Author</span>
                  <span className="font-medium">{scenario.author}</span>
                </div>
              </div>
            </div>

            <div className="pt-6 border-t border-border">
              <button
                onClick={() => setShowLaunchDialog(true)}
                disabled={isLaunching}
                className="w-full inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
              >
                {isLaunching ? (
                  <LoadingSpinner size="sm" className="text-primary-foreground" />
                ) : (
                  <Play className="h-4 w-4 fill-current" />
                )}
                {isInProgress ? 'Resume Scenario' : 'Launch Scenario'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Launch Confirmation Dialog */}
      {showLaunchDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-md rounded-xl border border-border bg-card p-6 shadow-xl space-y-6">
            <div>
              <h2 className="text-xl font-semibold mb-2">Launch Scenario?</h2>
              <p className="text-sm text-muted-foreground">
                You are about to deploy an isolated environment for <strong>{scenario.title}</strong>. This will allocate resources and start the timer.
              </p>
            </div>
            
            <div className="space-y-3 p-4 bg-muted/30 rounded-lg text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Difficulty:</span>
                <span className="font-medium">{scenario.difficulty}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Estimated Time:</span>
                <span className="font-medium">{scenario.estimatedTime}</span>
              </div>
            </div>

            <div className="flex gap-3 justify-end">
              <button 
                onClick={() => setShowLaunchDialog(false)}
                className="px-4 py-2 rounded-md text-sm font-medium hover:bg-muted transition-colors"
                disabled={isLaunching}
              >
                Cancel
              </button>
              <button 
                onClick={handleLaunch}
                disabled={isLaunching}
                className="px-4 py-2 rounded-md text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 transition-colors flex items-center gap-2"
              >
                {isLaunching ? 'Launching...' : 'Launch'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
