import React from 'react'

interface ScenarioReportBuilderProps {
  scenarioStateId: string
}

export function ScenarioReportBuilder({ scenarioStateId }: ScenarioReportBuilderProps) {
  return (
    <div className="bg-card text-card-foreground p-6 rounded-lg shadow-sm border mb-8">
      <h2 className="text-2xl font-bold mb-4">Scenario Report Builder</h2>
      <p className="text-muted-foreground mb-4">
        Review the automatically collected evidence and metrics below. You must complete the analysis and recommendations before submitting.
      </p>
      
      {/* Draft will be loaded here from /api/v1/reports/draft/{scenarioStateId} */}
      <div className="bg-muted p-4 rounded-md mb-6 whitespace-pre-wrap font-mono text-sm">
        [Loading AI-Generated Draft...]
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Final Analysis</label>
          <textarea 
            className="w-full h-32 p-3 rounded-md bg-background border text-foreground"
            placeholder="Provide your final technical analysis here..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Recommendations</label>
          <textarea 
            className="w-full h-32 p-3 rounded-md bg-background border text-foreground"
            placeholder="Provide remediation recommendations here..."
          />
        </div>
        
        <div className="flex justify-end gap-2">
          <button className="px-4 py-2 border rounded-md hover:bg-muted">Save Draft</button>
          <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90">Submit Report</button>
        </div>
      </div>
    </div>
  )
}
