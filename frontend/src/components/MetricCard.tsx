import React from 'react';

interface MetricCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon?: React.ReactNode;
  highlight?: boolean;
}

export default function MetricCard({ title, value, subtitle, icon, highlight = false }: MetricCardProps) {
  return (
    <div className={`relative overflow-hidden rounded-xl p-6 bg-slate-900/50 border shadow-sm transition-all duration-300 hover:bg-slate-800/50 flex flex-col justify-between h-full ${highlight ? 'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.1)]' : 'border-slate-800'}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-widest">{title}</h3>
        {icon && (
          <div className={`w-8 h-8 flex items-center justify-center rounded-lg ${highlight ? 'bg-red-500/10 text-red-400' : 'bg-cyan-500/10 text-cyan-400'}`}>
            {icon}
          </div>
        )}
      </div>
      <div>
        <div className="flex items-baseline gap-2">
          <span className={`text-4xl font-light tracking-tight ${highlight ? 'text-red-400' : 'text-slate-100'}`}>{value}</span>
        </div>
        {subtitle && <p className="mt-2 text-sm text-slate-500 font-medium">{subtitle}</p>}
      </div>
    </div>
  )
}
