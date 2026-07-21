import { Search } from 'lucide-react'

export function SearchBar() {
  return (
    <div className="relative hidden lg:flex items-center w-64 lg:w-80 group">
      <Search className="absolute left-2.5 h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
      <input
        type="text"
        placeholder="Search..."
        className="h-9 w-full rounded-md border border-input bg-background/50 pl-9 pr-12 text-sm shadow-sm transition-all placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary focus-visible:bg-background"
      />
      <div className="absolute right-2 flex items-center gap-1">
        <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
          <span className="text-xs">Ctrl</span>K
        </kbd>
      </div>
    </div>
  )
}
