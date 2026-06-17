import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-cyan-900 selection:text-cyan-50">
      
      {/* Background Glow Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-cyan-900/20 blur-[120px]"></div>
        <div className="absolute top-[20%] -right-[10%] w-[40%] h-[60%] rounded-full bg-blue-900/10 blur-[100px]"></div>
      </div>

      <div className="relative max-w-6xl mx-auto px-6 py-24 sm:py-32 flex flex-col items-center justify-center min-h-screen">
        
        {/* Hero Section */}
        <div className="text-center max-w-3xl mb-16 space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-semibold text-cyan-400 mb-4 tracking-wide shadow-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </span>
            SISTEMA ACTIVO
          </div>
          
          <h1 className="text-5xl sm:text-7xl font-extrabold tracking-tight text-white mb-6">
            VisionMeteor <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">v11</span>
          </h1>
          
          <p className="text-lg sm:text-xl text-slate-400 font-medium leading-relaxed max-w-2xl mx-auto">
            Plataforma de Diagnóstico Meteorológico Satelital impulsada por Machine Learning.
          </p>
        </div>

        {/* CTA Button */}
        <div className="mb-24 relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
          <Link 
            href="/dashboard"
            className="relative flex items-center gap-3 px-8 py-4 bg-slate-900 border border-slate-700 hover:border-cyan-500/50 rounded-xl transition-all duration-300 shadow-xl group-hover:shadow-cyan-900/20"
          >
            <span className="text-xl">🚀</span>
            <span className="text-white font-semibold tracking-wide text-lg">Iniciar Motor de Análisis</span>
          </Link>
        </div>

        {/* Info Cards Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
          
          {/* Card 1 */}
          <div className="p-8 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-md shadow-sm hover:border-slate-700 transition-colors">
            <div className="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center mb-6 text-cyan-400">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-slate-200 mb-3">Captura SDR</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Intercepción de telemetría de satélites NOAA y Meteor M2 mediante antenas RTL-SDR.
            </p>
          </div>

          {/* Card 2 */}
          <div className="p-8 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-md shadow-sm hover:border-slate-700 transition-colors">
            <div className="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center mb-6 text-blue-400">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H7.5a2.25 2.25 0 00-2.25 2.25v10.5a2.25 2.25 0 002.25 2.25z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-slate-200 mb-3">Motor IA</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Clasificación espacial automática utilizando K-Means Clustering y tensores 4D termodinámicos.
            </p>
          </div>

          {/* Card 3 */}
          <div className="p-8 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-md shadow-sm hover:border-slate-700 transition-colors">
            <div className="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center mb-6 text-orange-400">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-slate-200 mb-3">Nowcasting</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Detección en tiempo real de convección profunda y amenazas meteorológicas severas.
            </p>
          </div>

        </div>
      </div>
    </main>
  );
}
