import { Users, Server, Wrench, ShieldAlert, Activity } from 'lucide-react'
import { PageHeader } from '@/components/common/PageHeader'
import { StatCard } from '@/components/common/StatCard'
import { InfoPanel } from '@/components/common/InfoPanel'
import { useDashboardSummary } from '@/hooks/api/useDashboard'
import { useRecentScenarios, useScenarios } from '@/hooks/api/useScenarios'
import { ScenarioCard } from '@/components/scenarios/ScenarioCard'
import { Link } from 'react-router-dom'

export function DashboardPage() {
  const { data: summary, isLoading, isError } = useDashboardSummary()
  const { data: scenarios = [] } = useScenarios()
  const { recent } = useRecentScenarios()

  // Derive recommended (e.g. Beginner scenarios not yet completed)
  // For simplicity, just grab the first two Beginner ones
  const recommendedScenarios = scenarios
    .filter(s => s.difficulty === 'Beginner' && s.status !== 'Completed')
    .slice(0, 2)
    
  const recentScenariosData = recent
    .map(id => scenarios.find(s => s.id === id))
    .filter(Boolean)
    .slice(0, 2)

  if (isLoading) {
    return (
      <div className="flex-1 p-8">
        <PageHeader title="Enterprise Overview" />
        <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4 animate-pulse">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-32 rounded-xl bg-card border border-border" />
          ))}
        </div>
      </div>
    )
  }

  if (isError || !summary) {
    return (
      <div className="flex-1 p-8">
        <PageHeader title="Enterprise Overview" />
        <div className="mt-8 rounded-xl border border-destructive/50 bg-destructive/10 p-6 text-destructive">
          Failed to load dashboard metrics. Please try again later.
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 p-4 md:p-8 space-y-8 animate-fade-in">
      <PageHeader 
        title="Enterprise Overview" 
        description="High-level metrics and system status across NeoFactory Industries."
      />

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Assets"
          value={summary.assets.total}
          icon={Server}
          variant="primary"
          trend={{ value: '12', isPositive: true }}
        />
        <StatCard
          title="Active Employees"
          value={summary.employees.active}
          icon={Users}
          variant="default"
        />
        <StatCard
          title="Open Maintenance"
          value={summary.tickets.open}
          icon={Wrench}
          variant={summary.tickets.open > 5 ? 'warning' : 'default'}
        />
        <StatCard
          title="Active Alerts"
          value="3"
          icon={ShieldAlert}
          variant="destructive"
          trend={{ value: '1', isPositive: false }}
        />
      </div>

      {/* Quick Status Panels */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <InfoPanel 
            title="System Status" 
            description="Real-time status of critical infrastructure components."
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between rounded-lg border border-border p-4 bg-muted/20">
                <div className="flex items-center gap-3">
                  <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="font-medium text-sm">Primary Factory Network</span>
                </div>
                <span className="text-xs text-muted-foreground">Optimal</span>
              </div>
              <div className="flex items-center justify-between rounded-lg border border-border p-4 bg-muted/20">
                <div className="flex items-center gap-3">
                  <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="font-medium text-sm">Authentication Services</span>
                </div>
                <span className="text-xs text-muted-foreground">Optimal</span>
              </div>
              <div className="flex items-center justify-between rounded-lg border border-amber-500/20 bg-amber-500/5 p-4">
                <div className="flex items-center gap-3">
                  <div className="h-2 w-2 rounded-full bg-amber-500 animate-pulse" />
                  <span className="font-medium text-sm text-amber-600 dark:text-amber-400">OT Gateway Node B</span>
                </div>
                <span className="text-xs text-amber-600 dark:text-amber-400">High Latency</span>
              </div>
            </div>
          </InfoPanel>
        </div>

        <div>
          <InfoPanel 
            title="Recent Activity" 
            description="Latest events across the platform."
          >
            <div className="space-y-4 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
              {/* Timeline Items - Mocked for now */}
              {[
                { time: '10m ago', text: 'Firmware updated on PLC-A1' },
                { time: '1h ago', text: 'New maintenance ticket #T-992' },
                { time: '3h ago', text: 'User "jdoe" provisioned' },
                { time: '5h ago', text: 'Weekly security scan completed' }
              ].map((item, i) => (
                <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-5 h-5 rounded-full border border-primary bg-background shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow">
                    <Activity className="h-2.5 w-2.5 text-primary" />
                  </div>
                  <div className="w-[calc(100%-2rem)] md:w-[calc(50%-1.5rem)] p-3 rounded-lg border border-border bg-card shadow-sm">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-xs text-foreground">{item.text}</span>
                    </div>
                    <div className="text-[10px] text-muted-foreground">{item.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </InfoPanel>
        </div>
      </div>

      {/* Cyber Range Integration */}
      <div className="grid gap-6 md:grid-cols-2 mt-8">
        {recentScenariosData.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold tracking-tight">Recent Scenarios</h2>
              <Link to="/scenarios" className="text-sm text-primary hover:underline">View All</Link>
            </div>
            <div className="grid gap-4">
              {recentScenariosData.map(s => (
                // @ts-ignore - s is guaranteed to be Scenario here
                <ScenarioCard key={s.id} scenario={s} />
              ))}
            </div>
          </div>
        )}

        {recommendedScenarios.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold tracking-tight">Recommended Scenarios</h2>
              <Link to="/scenarios" className="text-sm text-primary hover:underline">Discover More</Link>
            </div>
            <div className="grid gap-4">
              {recommendedScenarios.map(s => (
                <ScenarioCard key={s.id} scenario={s} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
