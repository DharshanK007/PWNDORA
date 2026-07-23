import { useState } from 'react'
import { ShieldAlert, ChevronRight, Send, AlertTriangle } from 'lucide-react'

// Stage objects are passed directly from scenario.stages[]
// Both OPF and SE (and any future scenario) work because fields come from YAML
interface ScenarioStage {
  id: number
  objective?: string
  owasp?: string
  mitre?: string
  vulnerability_category?: string
  enterprise_layer?: string
  attack_surface?: string
}

interface PostLabAssessmentDialogProps {
  isOpen: boolean
  completedStages: ScenarioStage[]
  onSubmit: () => void
  onCancel: () => void
}

const CVSS_FACTORS = [
  { id: 'AV', label: 'Attack Vector', desc: 'Network vs Local access?', options: ['Network', 'Local'] },
  { id: 'PR', label: 'Privileges Required', desc: 'Auth level needed?', options: ['Unauthenticated', 'Normal User', 'Admin'] },
  { id: 'C', label: 'Confidentiality', desc: 'Can they steal data?', options: ['High', 'Low', 'None'] },
  { id: 'I', label: 'Integrity', desc: 'Can they modify data?', options: ['High', 'Low', 'None'] },
  { id: 'A', label: 'Availability', desc: 'Can they crash it?', options: ['High', 'Low', 'None'] },
]

const OWASP_LIKELIHOOD = [
  { id: 'L_Skill', label: 'Skill Level', desc: '0=Expert, 5=User, 9=None', options: ['0', '5', '9'] },
  { id: 'L_Motive', label: 'Motive', desc: '1=Low, 4=Theft, 9=High', options: ['1', '4', '9'] },
  { id: 'L_Opp', label: 'Opportunity', desc: '0=Custom, 4=Internet, 9=Any', options: ['0', '4', '9'] },
  { id: 'L_Size', label: 'Size', desc: '2=Insider, 7=Auth, 9=Anon', options: ['2', '7', '9'] },
  { id: 'L_Disc', label: 'Ease of Discovery', desc: '1=Hard, 3=Diff, 7=Easy, 9=Auto', options: ['1', '3', '7', '9'] },
  { id: 'L_Exp', label: 'Ease of Exploit', desc: '1=Hard, 3=Diff, 5=Easy, 9=Auto', options: ['1', '3', '5', '9'] },
  { id: 'L_Aware', label: 'Awareness', desc: '1=Zero, 5=Hidden, 6=Known, 9=Pub', options: ['1', '5', '6', '9'] },
  { id: 'L_Detect', label: 'Intrusion Detect', desc: '1=Block, 3=Log, 8=NoRev, 9=None', options: ['1', '3', '8', '9'] }
]

const OWASP_IMPACT = [
  { id: 'I_Conf', label: 'Loss of Conf', desc: '2=Min, 6=Crit, 9=All', options: ['2', '6', '9'] },
  { id: 'I_Integ', label: 'Loss of Integ', desc: '1=Min, 5=Crit, 9=All', options: ['1', '5', '9'] },
  { id: 'I_Avail', label: 'Loss of Avail', desc: '1=Min, 5=Crit, 9=All', options: ['1', '5', '9'] },
  { id: 'I_Acct', label: 'Loss of Acct', desc: '1=Trace, 7=Poss, 9=Anon', options: ['1', '7', '9'] },
  { id: 'I_Fin', label: 'Financial Dmg', desc: '1=Low, 3=Min, 7=Bankrupt, 9=Col', options: ['1', '3', '7', '9'] },
  { id: 'I_Rep', label: 'Reputation Dmg', desc: '1=Min, 4=Cust, 5=Brand, 9=Dest', options: ['1', '4', '5', '9'] },
  { id: 'I_Comp', label: 'Non-Compliance', desc: '1=Min, 2=Clear, 5=High, 7=Max', options: ['1', '2', '5', '7'] },
  { id: 'I_Priv', label: 'Privacy Viol', desc: '3=One, 5=100s, 7=Mills, 9=All', options: ['3', '5', '7', '9'] }
]

export function PostLabAssessmentDialog({ isOpen, completedStages, onSubmit, onCancel }: PostLabAssessmentDialogProps) {
  const [currentStageIndex, setCurrentStageIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, Record<string, string>>>({})

  if (!isOpen) return null

  // If no stages completed, just show a submit screen
  if (completedStages.length === 0) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in">
        <div className="bg-card w-full max-w-md rounded-xl border border-border shadow-2xl overflow-hidden p-6 text-center">
          <ShieldAlert className="h-10 w-10 text-primary mx-auto mb-4" />
          <h2 className="text-xl font-bold mb-2">Lab Terminated</h2>
          <p className="text-muted-foreground mb-6">You ended the session before capturing any flags. No assessment required.</p>
          <button onClick={onSubmit} className="w-full bg-primary text-primary-foreground py-2 rounded-md font-semibold">End Session Now</button>
        </div>
      </div>
    )
  }

  const currentStage = completedStages[currentStageIndex]
  const isLastStage = currentStageIndex === completedStages.length - 1

  const handleSelect = (metric: string, value: string) => {
    setAnswers(prev => ({
      ...prev,
      [currentStage.id]: {
        ...prev[currentStage.id],
        [metric]: value
      }
    }))
  }

  const isCurrentStageComplete = () => {
    const stageAnswers = answers[currentStage?.id]
    if (!stageAnswers) return false
    const cvssDone = CVSS_FACTORS.every(f => !!stageAnswers[f.id])
    const lDone = OWASP_LIKELIHOOD.every(f => !!stageAnswers[f.id])
    const iDone = OWASP_IMPACT.every(f => !!stageAnswers[f.id])
    return cvssDone && lDone && iDone
  }

  const handleNext = () => {
    if (isLastStage) {
      onSubmit()
    } else {
      setCurrentStageIndex(prev => prev + 1)
    }
  }

  const renderSection = (title: string, factors: any[], bgClass: string) => (
    <div className={`p-4 rounded-lg border border-border ${bgClass} space-y-4`}>
      <h4 className="font-semibold text-sm text-foreground flex items-center gap-2">
        <AlertTriangle className="h-4 w-4 text-primary" /> {title}
      </h4>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {factors.map(f => (
          <div key={f.id} className="space-y-1.5">
            <label className="text-xs font-bold block text-muted-foreground">{f.label}</label>
            <p className="text-[10px] text-muted-foreground/80 leading-tight mb-2 h-6">{f.desc}</p>
            <div className="flex gap-1.5 flex-wrap">
              {f.options.map((val: string) => (
                <button
                  key={val}
                  onClick={() => handleSelect(f.id, val)}
                  className={`py-1 px-2.5 rounded text-xs font-medium border transition-colors ${
                    answers[currentStage.id]?.[f.id] === val 
                      ? 'bg-primary text-primary-foreground border-primary' 
                      : 'bg-background hover:bg-muted border-border text-foreground'
                  }`}
                >
                  {val}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in">
      <div className="bg-card w-full max-w-4xl rounded-xl border border-border shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        <div className="bg-primary/10 border-b border-primary/20 p-5 flex items-center gap-3 shrink-0">
          <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center">
            <ShieldAlert className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-foreground">Post-Lab Vulnerability Assessment</h2>
            <p className="text-sm text-muted-foreground">Map CVSS & OWASP Metrics for each exploited chain component.</p>
          </div>
        </div>

        <div className="flex bg-muted/30 border-b border-border shrink-0">
          {completedStages.map((stage, idx) => (
            <div 
              key={stage.id} 
              className={`flex-1 p-3 text-center text-xs font-semibold border-r border-border last:border-0 transition-colors ${
                idx === currentStageIndex ? 'bg-primary/10 text-primary border-b-2 border-b-primary' : 
                idx < currentStageIndex ? 'text-muted-foreground bg-muted/50' : 'text-muted-foreground/40'
              }`}
            >
              Step {idx + 1}: {stage.objective ?? `Stage ${stage.id}`}
            </div>
          ))}
        </div>

        <div className="p-6 overflow-y-auto flex-1 space-y-6">
          <div className="mb-2">
            <h3 className="text-lg font-semibold text-primary mb-1">
              Evaluating: {currentStage.objective ?? `Stage ${currentStage.id}`}
            </h3>
            <span className="text-xs font-mono bg-muted px-2 py-1 rounded text-muted-foreground">
              Vulnerability: {currentStage.owasp ?? currentStage.vulnerability_category ?? 'Unknown'}
            </span>
          </div>

          {renderSection('CVSS v3.1 Base Metrics', CVSS_FACTORS, 'bg-muted/10')}
          {renderSection('OWASP Risk Likelihood (Threat & Vuln)', OWASP_LIKELIHOOD, 'bg-amber-500/5 border-amber-500/20')}
          {renderSection('OWASP Risk Impact (Tech & Business)', OWASP_IMPACT, 'bg-destructive/5 border-destructive/20')}

        </div>

        <div className="p-4 border-t border-border bg-muted/40 flex justify-between items-center shrink-0">
          <button 
            onClick={onCancel}
            className="text-sm font-medium text-muted-foreground hover:text-foreground px-4 py-2"
          >
            Cancel
          </button>
          
          <button
            onClick={handleNext}
            disabled={!isCurrentStageComplete()}
            className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-5 py-2.5 rounded-md font-semibold text-sm hover:bg-primary/90 disabled:opacity-50 transition-all"
          >
            {isLastStage ? (
              <>
                Submit & End Session <Send className="h-4 w-4" />
              </>
            ) : (
              <>
                Next Stage <ChevronRight className="h-4 w-4" />
              </>
            )}
          </button>
        </div>

      </div>
    </div>
  )
}
