import React from 'react'

export function HintButton() {
  return (
    <div className="mt-4 p-4 bg-muted rounded-md border">
      <h3 className="font-semibold mb-2">Need a Hint?</h3>
      <p className="text-sm text-muted-foreground mb-3">
        Our AI Mentor can give you a subtle nudge based on your current progress.
      </p>
      <button className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm hover:bg-secondary/80">
        Ask Mentor
      </button>
    </div>
  )
}
