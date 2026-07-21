import { useState } from 'react'
import { PageHeader } from '@/components/common/PageHeader'
import { InfoPanel } from '@/components/common/InfoPanel'

type SettingsTab = 'general' | 'appearance' | 'security'

export function SettingsPage() {
  const [activeTab, setActiveTab] = useState<SettingsTab>('general')

  return (
    <div className="flex-1 space-y-6">
      <PageHeader 
        title="Settings" 
        description="Manage your enterprise preferences and account configurations."
      />

      <div className="flex flex-col md:flex-row gap-6">
        {/* Settings Navigation */}
        <nav className="flex md:flex-col gap-1 w-full md:w-64 shrink-0 overflow-x-auto pb-2 md:pb-0 custom-scrollbar">
          <button
            onClick={() => setActiveTab('general')}
            className={`px-4 py-2 text-sm font-medium rounded-lg text-left whitespace-nowrap transition-colors ${
              activeTab === 'general'
                ? 'bg-primary text-primary-foreground shadow'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            General Profile
          </button>
          <button
            onClick={() => setActiveTab('appearance')}
            className={`px-4 py-2 text-sm font-medium rounded-lg text-left whitespace-nowrap transition-colors ${
              activeTab === 'appearance'
                ? 'bg-primary text-primary-foreground shadow'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            Appearance
          </button>
          <button
            onClick={() => setActiveTab('security')}
            className={`px-4 py-2 text-sm font-medium rounded-lg text-left whitespace-nowrap transition-colors ${
              activeTab === 'security'
                ? 'bg-primary text-primary-foreground shadow'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            Security & Login
          </button>
        </nav>

        {/* Settings Content */}
        <div className="flex-1">
          <InfoPanel title={
            activeTab === 'general' ? 'General Profile' :
            activeTab === 'appearance' ? 'Appearance' :
            'Security & Login'
          }>
            {activeTab === 'general' && (
              <div className="space-y-4 max-w-md">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-foreground">Email Address</label>
                  <input 
                    type="email" 
                    defaultValue="ceo@neofactory.com"
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-foreground">Display Name</label>
                  <input 
                    type="text" 
                    defaultValue="Alice Administrator"
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50"
                  />
                </div>
                <button className="mt-4 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors">
                  Save Changes
                </button>
              </div>
            )}

            {activeTab === 'appearance' && (
              <div className="space-y-4 max-w-md">
                <p className="text-sm text-muted-foreground mb-4">
                  Theme settings can also be modified from the top right user menu.
                </p>
                <div className="flex items-center justify-between p-4 rounded-lg border border-border">
                  <div>
                    <h4 className="text-sm font-medium text-foreground">Compact Mode</h4>
                    <p className="text-xs text-muted-foreground">Reduce spacing in data tables.</p>
                  </div>
                  <div className="h-5 w-9 rounded-full bg-muted border border-border relative cursor-pointer">
                    <div className="h-4 w-4 rounded-full bg-background absolute left-0.5 top-0.5 shadow-sm" />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'security' && (
              <div className="space-y-4 max-w-md">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-foreground">Current Password</label>
                  <input 
                    type="password" 
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-foreground">New Password</label>
                  <input 
                    type="password" 
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                  />
                </div>
                <button className="mt-4 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors">
                  Update Password
                </button>
              </div>
            )}
          </InfoPanel>
        </div>
      </div>
    </div>
  )
}
