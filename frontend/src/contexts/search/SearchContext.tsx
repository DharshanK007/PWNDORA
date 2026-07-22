import { createContext, useContext, useState, ReactNode } from 'react'

export type SearchScope = 'enterprise' | 'scenario' | 'workspace' | 'global'

interface SearchContextValue {
  isOpen: boolean
  query: string
  scope: SearchScope
  openSearch: (scope?: SearchScope) => void
  closeSearch: () => void
  setQuery: (query: string) => void
}

const SearchContext = createContext<SearchContextValue | undefined>(undefined)

export function SearchProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [scope, setScope] = useState<SearchScope>('global')

  const openSearch = (newScope: SearchScope = 'global') => {
    setScope(newScope)
    setIsOpen(true)
  }

  const closeSearch = () => {
    setIsOpen(false)
    setQuery('')
  }

  return (
    <SearchContext.Provider
      value={{
        isOpen,
        query,
        scope,
        openSearch,
        closeSearch,
        setQuery,
      }}
    >
      {children}
    </SearchContext.Provider>
  )
}

export function useSearch() {
  const context = useContext(SearchContext)
  if (context === undefined) {
    throw new Error('useSearch must be used within a SearchProvider')
  }
  return context
}
