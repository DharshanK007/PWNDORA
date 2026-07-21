export interface Evidence {
  id: string
  name: string
  type: 'log' | 'image' | 'text' | 'pdf' | 'pcap' | 'memory' | 'json' | 'yaml'
  size: number
  source: string
  addedAt: string
  content?: string // For text-based evidence
  url?: string // For binary/image evidence
}

export interface TimelineEvent {
  id: string
  timestamp: string
  type: 'INFO' | 'SUCCESS' | 'WARNING' | 'ERROR'
  message: string
}

export interface PanelSizes {
  left: number // Percentage width
  right: number // Percentage width
  bottom: number // Percentage height (for log viewer)
}

export interface CollapsedPanels {
  left: boolean
  right: boolean
  bottom: boolean
}

export interface WorkspaceLayout {
  sizes: PanelSizes
  collapsed: CollapsedPanels
}

export interface WorkspaceState {
  scenarioId: string
  layout: WorkspaceLayout
  openFiles: string[] // Evidence IDs
  selectedEvidenceId: string | null
  notes: string
  timeline: TimelineEvent[]
}
