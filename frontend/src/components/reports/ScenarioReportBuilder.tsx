import { useEffect, useState } from 'react'
import { REMEDIATION_CHIPS } from '../../constants/remediations'
import api from '@/lib/axios'

interface ScenarioReportBuilderProps {
  scenarioStateId: string
}

interface ReportDraft {
  id: string
  title: string
  content: string
  status: string
}

interface FindingContent {
  id: string
  title: string
  rawMarkdown: string
  analysis: string
  recommendation: string
  category: string
}

export function ScenarioReportBuilder({ scenarioStateId }: ScenarioReportBuilderProps) {
  const [draft, setDraft] = useState<ReportDraft | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  const [introMarkdown, setIntroMarkdown] = useState<string>('')
  const [findings, setFindings] = useState<FindingContent[]>([])
  
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    async function fetchDraft() {
      try {
        const response = await api.get(`/reports/draft/${scenarioStateId}`)
        const data = response.data
        setDraft(data)
        
        // Parse the markdown. Find "### Finding #X" blocks.
        const parts = data.content.split('### Finding #')
        setIntroMarkdown(parts[0])
        
        if (parts.length > 1) {
          const parsedFindings: FindingContent[] = parts.slice(1).map((part: string) => {
            const firstNewlineIndex = part.indexOf('\n')
            const titleLine = part.slice(0, firstNewlineIndex).trim()
            const rest = part.slice(firstNewlineIndex)
            const id = titleLine.split(':')[0]
            
            // Extract OWASP Classification to use for category lookup
            const owaspMatch = rest.match(/OWASP Classification\*\*: (.*?)\n/)
            let category = 'default'
            if (owaspMatch) {
               const owaspStr = owaspMatch[1].toLowerCase()
               if (owaspStr.includes('injection')) category = 'injection'
               else if (owaspStr.includes('broken access control')) category = 'authorization'
               else if (owaspStr.includes('authentication')) category = 'authentication'
            }

            return {
              id,
              title: titleLine,
              rawMarkdown: `### Finding #${part}`,
              analysis: '',
              recommendation: '',
              category
            }
          })
          
          // Only override empty strings with previously saved text if available
          // Since the backend doesn't store per-finding text separately (it stores one big summary),
          // For this pilot, we'll extract it if it's there. 
          // Since it's appended at the end of the markdown...
          // A robust way would be to parse the [Write your technical analysis here] blocks, but the user is fine 
          // with a simple approach for the prototype. We'll leave them empty for now unless it's already filled.
          setFindings(parsedFindings)
        }
      } catch (err: any) {
        if (err.response?.status === 404) {
           setError("No completed stages to generate a report.")
        } else {
           setError(err.message)
        }
      } finally {
        setLoading(false)
      }
    }
    fetchDraft()
  }, [scenarioStateId])

  const handleSave = async (submit: boolean = false) => {
    if (!draft) return
    setIsSaving(true)
    
    // Reconstruct the full markdown
    let updatedContent = introMarkdown
    findings.forEach(f => {
      // replace the placeholders or previous text with the new text
      let findingMd = f.rawMarkdown
      
      findingMd = findingMd.replace(/\[Write your technical analysis here\]|#### Analyst Technical Assessment\n.*?(?=#### Remediation & Control Guidance)/s, `#### Analyst Technical Assessment\n${f.analysis || '[Write your technical analysis here]'}\n\n`)
      findingMd = findingMd.replace(/\[Write remediation recommendations here\]|#### Remediation & Control Guidance\n.*/s, `#### Remediation & Control Guidance\n${f.recommendation || '[Write remediation recommendations here]'}\n\n`)
      
      updatedContent += findingMd
    })

    try {
      const status = submit ? "Under Review" : "Draft"
      await api.patch(`/reports/${draft.id}/submit`, { summary: updatedContent, status })
      setDraft({ ...draft, content: updatedContent, status })
    } catch (err: any) {
      alert("Failed to save report: " + err.message)
    } finally {
      setIsSaving(false)
    }
  }
  
  const allComplete = findings.every(f => f.analysis.trim() !== '' && f.recommendation.trim() !== '')

  if (loading) return <div className="p-6">Loading Draft...</div>
  if (error) return <div className="p-6 text-red-500">{error}</div>

  return (
    <div className="bg-card text-card-foreground p-6 rounded-lg shadow-sm border mb-8">
      <h2 className="text-2xl font-bold mb-4">Scenario Report Builder</h2>
      <p className="text-muted-foreground mb-4">
        Review the automatically collected evidence and metrics below. You must complete the analysis and recommendations before submitting.
      </p>
      
      <div className="bg-muted p-4 rounded-md mb-6 whitespace-pre-wrap font-mono text-sm">
        {introMarkdown}
      </div>

      <div className="space-y-8">
        {findings.map((f, i) => (
          <div key={f.id} className="border border-border rounded-xl p-5 bg-muted/10">
             <h3 className="text-lg font-semibold mb-2 text-primary">Finding #{f.title}</h3>
             
             {/* The auto-assembled facts for this finding */}
             <div className="bg-muted/30 p-3 rounded-md mb-4 text-xs font-mono whitespace-pre-wrap">
               {f.rawMarkdown.split('#### Analyst Technical Assessment')[0]}
             </div>
             
             <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Analysis</label>
                <textarea 
                  className="w-full h-24 p-3 rounded-md bg-background border text-foreground"
                  placeholder="Provide your final technical analysis here..."
                  value={f.analysis}
                  onChange={(e) => {
                    const newFindings = [...findings]
                    newFindings[i].analysis = e.target.value
                    setFindings(newFindings)
                  }}
                />
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium">Recommendations</label>
                  <div className="flex gap-2">
                    {REMEDIATION_CHIPS[f.category]?.map((chip, idx) => (
                      <button 
                        key={idx}
                        onClick={() => {
                          const newFindings = [...findings]
                          newFindings[i].recommendation += (newFindings[i].recommendation ? '\n- ' : '- ') + chip
                          setFindings(newFindings)
                        }}
                        className="text-[10px] bg-primary/10 text-primary hover:bg-primary/20 px-2 py-1 rounded-full transition-colors"
                      >
                        + {chip}
                      </button>
                    ))}
                  </div>
                </div>
                <textarea 
                  className="w-full h-24 p-3 rounded-md bg-background border text-foreground"
                  placeholder="Provide remediation recommendations here..."
                  value={f.recommendation}
                  onChange={(e) => {
                    const newFindings = [...findings]
                    newFindings[i].recommendation = e.target.value
                    setFindings(newFindings)
                  }}
                />
              </div>
            </div>
          </div>
        ))}
        
        {findings.length > 0 && (
          <div className="flex justify-end gap-3 pt-4 border-t border-border">
            <button 
              onClick={() => handleSave(false)} 
              disabled={isSaving}
              className="px-4 py-2 border rounded-md hover:bg-muted"
            >
              {isSaving ? 'Saving...' : 'Save Draft'}
            </button>
            <button 
              onClick={() => handleSave(true)} 
              disabled={!allComplete || isSaving}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit Report
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
