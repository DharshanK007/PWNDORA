import { BaseSkeleton } from './BaseSkeleton'

export function WorkspaceSkeleton() {
  return (
    <div className="flex h-screen w-full flex-col bg-background overflow-hidden animate-in fade-in duration-500">
      <div className="h-14 border-b border-border flex items-center px-4 justify-between bg-card">
        <BaseSkeleton className="h-6 w-32" />
        <div className="flex items-center gap-4">
          <BaseSkeleton className="h-6 w-24" />
          <BaseSkeleton className="h-8 w-8 rounded-full" />
        </div>
      </div>
      
      <div className="h-10 border-b border-border flex items-center px-4 gap-4 bg-muted/20">
        <BaseSkeleton className="h-6 w-16" />
        <BaseSkeleton className="h-6 w-16" />
        <BaseSkeleton className="h-6 w-16" />
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel */}
        <div className="w-[25%] flex flex-col border-r border-border">
          <div className="flex-1 p-4 flex flex-col gap-3">
            <BaseSkeleton className="h-6 w-32 mb-2" />
            <BaseSkeleton className="h-16 w-full rounded-md" />
            <BaseSkeleton className="h-16 w-full rounded-md" />
            <BaseSkeleton className="h-16 w-full rounded-md" />
          </div>
          <div className="h-[40%] border-t border-border p-4">
            <BaseSkeleton className="h-6 w-24 mb-4" />
            <BaseSkeleton className="h-full w-full rounded-md" />
          </div>
        </div>

        {/* Center Panel */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 p-8 flex items-center justify-center">
            <BaseSkeleton className="h-64 w-3/4 max-w-2xl rounded-xl" />
          </div>
          <div className="h-[30%] border-t border-border p-4 flex flex-col gap-2">
            <BaseSkeleton className="h-6 w-20 mb-2" />
            <BaseSkeleton className="h-4 w-[60%]" />
            <BaseSkeleton className="h-4 w-[80%]" />
            <BaseSkeleton className="h-4 w-[70%]" />
            <BaseSkeleton className="h-4 w-[50%]" />
          </div>
        </div>

        {/* Right Panel */}
        <div className="w-[20%] flex flex-col border-l border-border">
          <div className="flex-1 p-4 flex flex-col gap-4">
            <BaseSkeleton className="h-6 w-24 mb-2" />
            <div className="flex items-start gap-3">
              <BaseSkeleton className="h-5 w-5 rounded-full" />
              <BaseSkeleton className="h-10 w-full" />
            </div>
            <div className="flex items-start gap-3">
              <BaseSkeleton className="h-5 w-5 rounded-full" />
              <BaseSkeleton className="h-10 w-full" />
            </div>
          </div>
          <div className="h-[40%] border-t border-border p-4 flex flex-col gap-4">
            <BaseSkeleton className="h-6 w-24 mb-2" />
            <BaseSkeleton className="h-12 w-full" />
            <BaseSkeleton className="h-12 w-full" />
          </div>
        </div>
      </div>
    </div>
  )
}
