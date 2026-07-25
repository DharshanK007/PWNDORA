import React from 'react';

export interface InfographicData {
  stage: number;
  matrix: number;
  time: number; // in seconds
}

interface ReportInfographicsProps {
  data: InfographicData[];
}

export const ReportInfographics: React.FC<ReportInfographicsProps> = ({ data }) => {
  if (!data || data.length === 0) return null;

  // Maximum values for scaling
  const maxTime = Math.max(...data.map(d => d.time), 600); // at least 10 minutes (600s) for scale

  // Format time beautifully (e.g. 10m 30s)
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}m ${s}s`;
  };

  return (
    <div className="pdf-infographics-container mb-8 space-y-8 bg-white text-slate-900 p-6 rounded-xl border border-slate-200" style={{ pageBreakInside: 'avoid' }}>
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">Lab Performance Analytics</h2>
        <p className="text-sm text-slate-500 mt-1">Detailed breakdown of learner efficiency and progression across stages.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* 1. Stage MATRIX Score Progression */}
        <div className="bg-slate-50 p-5 rounded-lg border border-slate-100 shadow-sm relative">
          <h3 className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2 uppercase tracking-wide">
            <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
            Matrix Score Progression
          </h3>
          
          <div className="relative h-48 w-full pl-8 pb-6 mt-4">
            {/* Y-axis labels */}
            <div className="absolute left-0 top-0 bottom-6 flex flex-col justify-between text-[10px] text-slate-400 font-mono items-end pr-2 font-medium">
              <span>100 ┤</span>
              <span>80 ┤</span>
              <span>60 ┤</span>
              <span>40 ┤</span>
              <span>20 ┤</span>
              <span>0 ┤</span>
            </div>
            
            {/* Grid lines */}
            <div className="absolute left-8 right-4 top-0 bottom-6 flex flex-col justify-between">
              {[100, 80, 60, 40, 20, 0].map((_, i) => (
                <div key={i} className="w-full border-b border-slate-200 border-dashed" style={{ height: '1px', marginTop: '-1px' }}></div>
              ))}
            </div>

            {/* Data Points & Lines */}
            <svg className="absolute left-8 right-4 top-0 bottom-6 w-[calc(100%-3rem)] h-full overflow-visible">
              {data.map((d, i) => {
                const x = `${(i / (Math.max(1, data.length - 1))) * 100}%`;
                const y = `${100 - (d.matrix)}%`;
                
                let nextX, nextY;
                if (i < data.length - 1) {
                  nextX = `${((i + 1) / (Math.max(1, data.length - 1))) * 100}%`;
                  nextY = `${100 - (data[i+1].matrix)}%`;
                }

                return (
                  <React.Fragment key={i}>
                    {i < data.length - 1 && (
                      <line x1={x} y1={y} x2={nextX} y2={nextY} stroke="#6366f1" strokeWidth="2" strokeDasharray="4 2" className="opacity-60" />
                    )}
                    <circle cx={x} cy={y} r="5" fill="#4f46e5" stroke="#ffffff" strokeWidth="2" className="shadow-sm drop-shadow-md" />
                    <text x={x} y={y} dy="-12" dx="0" textAnchor="middle" fontSize="10" fill="#1e293b" fontWeight="bold">
                      {d.matrix.toFixed(1)}
                    </text>
                  </React.Fragment>
                );
              })}
            </svg>
            
            {/* X-axis labels */}
            <div className="absolute left-8 right-4 bottom-0 h-6 flex justify-between items-end pb-1 px-1">
              {data.map((d, i) => (
                <span key={i} className="text-[10px] text-slate-500 font-bold -ml-2">S{d.stage}</span>
              ))}
            </div>
          </div>
        </div>

        {/* 2. Time Distribution */}
        <div className="bg-slate-50 p-5 rounded-lg border border-slate-100 shadow-sm">
          <h3 className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2 uppercase tracking-wide">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            Time Distribution
          </h3>
          
          <div className="space-y-4 mt-6">
            {data.map((d, i) => {
              const widthPct = Math.min(100, Math.max(2, (d.time / maxTime) * 100));
              return (
                <div key={i} className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-end text-xs">
                    <span className="font-semibold text-slate-700">Stage {d.stage}</span>
                    <span className="text-[10px] font-mono text-slate-500">{formatTime(d.time)}</span>
                  </div>
                  <div className="h-4 w-full bg-slate-200 rounded-full overflow-hidden flex shadow-inner">
                    <div 
                      className="h-full bg-gradient-to-r from-emerald-400 to-emerald-600 rounded-full shadow-sm relative transition-all duration-1000"
                      style={{ width: `${widthPct}%` }}
                    >
                      <div className="absolute inset-0 bg-white/20" style={{ backgroundImage: 'linear-gradient(45deg, transparent 25%, rgba(255,255,255,0.15) 25%, rgba(255,255,255,0.15) 50%, transparent 50%, transparent 75%, rgba(255,255,255,0.15) 75%, rgba(255,255,255,0.15) 100%)', backgroundSize: '1rem 1rem' }}></div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          
          <div className="mt-4 pt-4 border-t border-slate-200 flex justify-between items-center">
            <span className="text-[10px] text-slate-400 font-medium">100% baseline = 10m 00s</span>
            <span className="text-xs font-bold text-emerald-600">Total: {formatTime(data.reduce((acc, curr) => acc + curr.time, 0))}</span>
          </div>
        </div>

      </div>
    </div>
  );
};
