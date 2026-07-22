import React, { useState } from 'react'
import { Search } from 'lucide-react'
import api from '@/lib/axios'

export function SearchBar() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any[] | null>(null)
  const [isSearching, setIsSearching] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const handleKeyDown = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && query.trim()) {
      setIsSearching(true)
      setShowResults(true)
      try {
        const { data } = await api.post('/search/', { query: query.trim() })
        setResults(data.items || [])
      } catch (err) {
        console.error('Search failed:', err)
        setResults([])
      } finally {
        setIsSearching(false)
      }
    }
  }

  return (
    <div className="relative hidden lg:flex items-center w-64 lg:w-80 group">
      <Search className="absolute left-2.5 h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        onFocus={() => results && setShowResults(true)}
        placeholder="Search... (Press Enter)"
        className="h-9 w-full rounded-md border border-input bg-background/50 pl-9 pr-12 text-sm shadow-sm transition-all placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary focus-visible:bg-background"
      />
      <div className="absolute right-2 flex items-center gap-1">
        <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
          <span className="text-xs">Ctrl</span>K
        </kbd>
      </div>

      {showResults && (
        <div className="absolute top-11 left-0 right-0 z-[100] rounded-xl border border-border bg-card/98 shadow-2xl p-3 backdrop-blur-md max-h-96 overflow-y-auto animate-in fade-in duration-150">
          <div className="flex items-center justify-between border-b border-border pb-2 mb-2 text-xs font-semibold text-muted-foreground">
            <span>Search Results for "{query}"</span>
            <button
              onClick={() => setShowResults(false)}
              className="text-xs text-muted-foreground hover:text-foreground"
            >
              Close
            </button>
          </div>

          {isSearching ? (
            <div className="p-4 text-center text-xs text-muted-foreground">Executing search...</div>
          ) : results && results.length > 0 ? (
            <div className="space-y-2">
              {results.map((item, idx) => (
                <div key={idx} className="p-2.5 rounded-lg border border-border/50 bg-muted/20 hover:bg-muted/40 transition-colors">
                  <div className="flex items-center justify-between text-xs font-medium text-primary">
                    <span>{item.title}</span>
                    <span className="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-primary/10 text-primary">
                      {item.category}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-foreground/80 font-mono leading-relaxed">{item.snippet}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 text-center text-xs text-muted-foreground">No records found. Try another query.</div>
          )}
        </div>
      )}
    </div>
  )
}
