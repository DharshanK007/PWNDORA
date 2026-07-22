import React from 'react'

export function LiveSessionsPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Live Cyber Range Sessions</h1>
      <div className="bg-card text-card-foreground border rounded-lg shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b bg-muted/50">
              <th className="p-4 font-medium text-muted-foreground">Session ID</th>
              <th className="p-4 font-medium text-muted-foreground">Learner</th>
              <th className="p-4 font-medium text-muted-foreground">Scenario</th>
              <th className="p-4 font-medium text-muted-foreground">Stage</th>
              <th className="p-4 font-medium text-muted-foreground">Status</th>
            </tr>
          </thead>
          <tbody>
            {/* Real implementation would map over API data here */}
            <tr className="border-b">
              <td className="p-4 font-mono text-sm">ssn_123abc</td>
              <td className="p-4">jane.doe@neofactory.local</td>
              <td className="p-4">Operation Phantom Firmware</td>
              <td className="p-4">
                <div className="w-full bg-secondary rounded-full h-2.5">
                  <div className="bg-primary h-2.5 rounded-full" style={{ width: "50%" }}></div>
                </div>
                <span className="text-xs text-muted-foreground mt-1 inline-block">Stage 2/4</span>
              </td>
              <td className="p-4">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
