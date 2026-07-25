import { ShieldAlert, Zap, Server, ChevronRight, Activity, Globe, Cpu } from 'lucide-react'
import { Link } from 'react-router-dom'
import { ROUTES } from '@/constants/routes'
import { AppLogo } from '@/components/common/AppLogo'
import { LabStatusBar } from '@/components/lab/LabStatusBar'

export function WelcomePage() {
  return (
    <div className="min-h-screen bg-background flex flex-col relative overflow-x-hidden">
      <LabStatusBar />
      {/* Background Decorators */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-[0.35] mix-blend-multiply pointer-events-none" 
        style={{ backgroundImage: 'url(/images/neo_factory_welcome_bg.png)' }} 
      />
      <div className="absolute inset-0 bg-gradient-to-b from-white/20 via-white/70 to-white pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-5 mix-blend-multiply pointer-events-none z-0" />
      
      {/* Top Bar */}
      <div className="relative z-10 w-full px-8 py-5 flex justify-between items-center border-b border-slate-200 bg-white/90 backdrop-blur-md">
        <AppLogo />
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-slate-500">
          <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          Systems Online
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 relative z-10 flex flex-col items-center justify-center p-6 text-center">
        <div className="max-w-5xl mx-auto space-y-16 animate-in fade-in slide-in-from-bottom-8 duration-700 mt-8">
          
          <div className="space-y-6">
            <div className="text-xs md:text-sm font-bold uppercase tracking-widest text-primary/80 bg-primary/10 border border-primary/20 px-4 py-1.5 rounded-full inline-block mb-2 shadow-xs">
              PWNDORA Vulnerability Chain Exploitation Lab
            </div>
            <h1 className="text-5xl md:text-7xl font-black tracking-tight text-slate-900">
              NeoFactory <span className="text-primary">Industries</span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto leading-relaxed font-light">
              Welcome to the digital operations center of a leading Global Industrial IoT Enterprise. You have been granted administrative clearance.
            </p>
          </div>

          {/* Narrative Cards */}
          <div className="grid md:grid-cols-3 gap-8 text-left mt-16">
            
            <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-xl border border-slate-200 shadow-sm transition-all duration-500 ease-out hover:scale-[1.15] hover:-translate-y-4 hover:z-50 hover:shadow-2xl cursor-default relative overflow-hidden origin-center">
              <div className="absolute top-0 left-0 w-1 h-full bg-blue-500 rounded-l-xl opacity-50" />
              <div className="text-xs font-bold text-slate-400 tracking-widest uppercase mb-4">Module 01</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Global Infrastructure</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Centralized command and control for NeoFactory's international manufacturing hubs. This portal provides real-time oversight of interconnected OT (Operational Technology) networks, automated assembly lines, and global supply chain logistics.
              </p>
            </div>

            <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-xl border border-slate-200 shadow-sm transition-all duration-500 ease-out hover:scale-[1.15] hover:-translate-y-4 hover:z-50 hover:shadow-2xl cursor-default relative overflow-hidden origin-center">
              <div className="absolute top-0 left-0 w-1 h-full bg-amber-500 rounded-l-xl opacity-50" />
              <div className="text-xs font-bold text-slate-400 tracking-widest uppercase mb-4">Module 02</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Access & Security</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                All activities within this portal are strictly monitored and logged. Access is governed by role-based architecture. Personnel are required to maintain strict compliance with NeoFactory Information Security Policy Directive v4.2.
              </p>
            </div>

            <div className="group bg-white/80 backdrop-blur-sm p-8 rounded-xl border border-slate-200 shadow-sm transition-all duration-500 ease-out hover:scale-[1.15] hover:-translate-y-4 hover:z-50 hover:shadow-2xl cursor-default relative overflow-hidden origin-center">
              <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500 rounded-l-xl opacity-50" />
              <div className="text-xs font-bold text-slate-400 tracking-widest uppercase mb-4">Module 03</div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">System Telemetry</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Review live system diagnostics, manage production server configurations, and maintain critical enterprise uptime. Ensure all operational metrics remain within designated safety thresholds to prevent manufacturing disruptions.
              </p>
            </div>

          </div>

          <div className="pt-12">
            <Link
              to={ROUTES.DASHBOARD}
              className="inline-flex items-center justify-center gap-3 rounded-xl text-lg font-bold transition-all bg-primary text-primary-foreground hover:bg-primary/90 hover:-translate-y-1 hover:shadow-lg h-14 px-10"
            >
              Acknowledged
              <ChevronRight className="h-6 w-6" />
            </Link>
          </div>

        </div>
      </main>
      
      {/* Footer */}
      <div className="relative z-10 w-full p-6 text-center text-sm text-slate-500 border-t border-slate-200 bg-white/80 backdrop-blur-md">
        © 2026 NeoFactory Industries. Authorized Access Only.
      </div>
    </div>
  )
}
