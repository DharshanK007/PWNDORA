import { useState } from 'react'
import { PageHeader } from '@/components/common/PageHeader'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { useScenarios, useScenarioCategories } from '@/hooks/api/useScenarios'
import { ScenarioCard } from '@/components/scenarios/ScenarioCard'
import { ScenarioFilterPanel } from '@/components/scenarios/ScenarioFilterPanel'
import { ScenarioSearch } from '@/components/scenarios/ScenarioSearch'
import { ScenarioStats } from '@/components/scenarios/ScenarioStats'

export function ScenarioCatalogPage() {
  const { data: scenarios = [], isLoading, isError } = useScenarios()
  const { data: categories = [] } = useScenarioCategories()
  
  // Note: we can derive difficulties directly or use a hook.
  // The service extracts them dynamically, but we can hardcode for consistent sorting
  const difficulties = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedDifficulty, setSelectedDifficulty] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('')

  if (isLoading) {
    return (
      <div className="flex-1 p-8">
        <PageHeader title="Scenario Catalog" />
        <div className="flex items-center justify-center h-[60vh]">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="flex-1 p-8">
        <PageHeader title="Scenario Catalog" />
        <div className="mt-8 rounded-xl border border-destructive/50 bg-destructive/10 p-6 text-destructive">
          Failed to load scenarios. Please try again later.
        </div>
      </div>
    )
  }

  const filteredScenarios = scenarios.filter(s => {
    const matchesSearch = s.title.toLowerCase().includes(searchQuery.toLowerCase()) || s.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory ? s.category === selectedCategory : true
    const matchesDifficulty = selectedDifficulty ? s.difficulty === selectedDifficulty : true
    const matchesStatus = selectedStatus ? (s.status || 'Not Started') === selectedStatus : true
    return matchesSearch && matchesCategory && matchesDifficulty && matchesStatus
  })

  const inProgress = scenarios.filter(s => s.status === 'In Progress').length
  const completed = scenarios.filter(s => s.status === 'Completed').length
  const recommended = scenarios.filter(s => s.difficulty === 'Beginner').length // simple mock

  return (
    <div className="flex-1 p-4 md:p-8 space-y-8 animate-fade-in">
      <PageHeader 
        title="Scenario Catalog" 
        description="Discover, learn, and practice cyber-security concepts across various domains."
      />

      <ScenarioStats 
        total={scenarios.length} 
        inProgress={inProgress} 
        completed={completed} 
        recommended={recommended} 
      />

      <div className="flex flex-col md:flex-row gap-4 p-4 rounded-xl border border-border bg-card">
        <ScenarioSearch value={searchQuery} onChange={setSearchQuery} />
        <ScenarioFilterPanel 
          categories={categories}
          difficulties={difficulties}
          selectedCategory={selectedCategory}
          selectedDifficulty={selectedDifficulty}
          selectedStatus={selectedStatus}
          onCategoryChange={setSelectedCategory}
          onDifficultyChange={setSelectedDifficulty}
          onStatusChange={setSelectedStatus}
        />
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        {filteredScenarios.map(scenario => (
          <ScenarioCard key={scenario.id} scenario={scenario} />
        ))}
        {filteredScenarios.length === 0 && (
          <div className="col-span-full py-12 text-center text-muted-foreground border border-dashed border-border rounded-xl">
            No scenarios found matching your filters.
          </div>
        )}
      </div>
    </div>
  )
}
