'use client';
import { useEffect, useState } from 'react';
import MetricCard from '@/components/MetricCard';
import Uploader from '@/components/Uploader';

const IconCloud = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z" /></svg>
);

const IconGlobe = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" /></svg>
);

const IconAlert = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
);

const IconPlay = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.348a1.125 1.125 0 010 1.971l-11.54 6.347c-.75.412-1.667-.13-1.667-.986V5.653z" /></svg>
);

const IconBarChart = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>
);

const IconImage = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" /></svg>
);

const IconDownload = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" /></svg>
);

const IconThermometer = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
);

export default function Home() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [activeTab, setActiveTab] = useState<'comparacion' | 'heatmap'>('comparacion');
  
  const [visibleFile, setVisibleFile] = useState<File | null>(null);
  const [irFile, setIrFile] = useState<File | null>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/reporte')
      .then(res => res.json())
      .then(data => {
        setReport(data);
        setLoading(false);
      })
      .catch(() => {
        // Mock data fallback
        setTimeout(() => {
          setReport({
            fecha: new Date().toISOString(),
            amenaza_principal: { clase: "TORMENTA", nivel: "AMENAZA ALTA" },
            estadisticas: {
                porcentaje_nubes_total: 45.2,
                porcentaje_superficie_total: 54.8,
                desglose_porcentajes: { MAR: 30.5, TIERRA: 24.3, NUBE_BAJA_MEDIA: 15.0, CIRROS: 10.2, TORMENTA: 20.0 }
            }
          });
          setLoading(false);
        }, 1500);
      });
  }, []);

  const handleAnalizar = async () => {
    if (!visibleFile || !irFile) return alert("Por favor seleccione ambas imágenes satelitales en el paso anterior.");
    
    setUploading(true);
    try {
      // 1. Sincronizar imágenes al backend
      const formData = new FormData();
      formData.append("visible", visibleFile);
      formData.append("infrarroja", irFile);

      const uploadRes = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData,
      });
      if (!uploadRes.ok) throw new Error("Error al sincronizar imágenes con el clúster.");
      
      setUploading(false);
      setAnalyzing(true);
      
      // 2. Ejecutar Análisis
      const res = await fetch('http://127.0.0.1:8000/api/analizar', { method: 'POST' });
      const data = await res.json();
      if (!res.ok || data.error) {
        throw new Error(data.message || 'Falló la conexión con el motor V11.');
      }
      setReport(data);
    } catch (error: any) {
      console.error(error);
      alert(error.message || 'Error en el sistema.');
    } finally {
      setUploading(false);
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0f172a]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
      </div>
    );
  }

  // Limpieza de caracteres no deseados en caso de que vengan del backend (ej. emojis antiguos)
  const cleanLevel = report.amenaza_principal.nivel.replace(/[^a-zA-Z0-9\s]/g, '').trim();

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#050505] to-black text-slate-200">
    <main className="min-h-screen p-8 md:p-16 max-w-7xl mx-auto flex flex-col font-sans relative z-10">
      <header className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-slate-800 pb-8">
        <div>
          <h1 className="text-4xl md:text-5xl font-bold text-slate-100 mb-3 tracking-tight">
            VisionMeteor
          </h1>
          <p className="text-lg text-slate-400 font-medium">
            Módulo de Análisis Satelital Avanzado
          </p>
        </div>
        <button 
          onClick={handleAnalizar} 
          disabled={analyzing || uploading}
          className="px-8 py-3 bg-gradient-to-r from-cyan-600 to-blue-700 hover:from-cyan-500 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold rounded-full transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)] hover:shadow-[0_0_30px_rgba(6,182,212,0.5)] flex items-center gap-3 text-sm tracking-wide"
        >
          {uploading ? (
            <>
               <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Sincronizando al Clúster...
            </>
          ) : analyzing ? (
            <>
               <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Procesando Matriz (V11)...
            </>
          ) : (
            <>
              <IconPlay />
              Sincronizar y Analizar
            </>
          )}
        </button>
      </header>

      <Uploader 
        visibleFile={visibleFile}
        irFile={irFile}
        setVisibleFile={setVisibleFile}
        setIrFile={setIrFile}
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard 
          title="Clasificación Principal" 
          value={report.amenaza_principal.clase} 
          subtitle={cleanLevel}
          icon={<IconAlert />}
          highlight={cleanLevel.includes('ALTA') || cleanLevel.includes('EXTREMA')}
        />
        <MetricCard 
          title="Cobertura Nubosa" 
          value={`${report.estadisticas.porcentaje_nubes_total.toFixed(1)}%`} 
          subtitle="Proporción detectada"
          icon={<IconCloud />}
        />
        <MetricCard 
          title="Superficie Despejada" 
          value={`${report.estadisticas.porcentaje_superficie_total.toFixed(1)}%`} 
          subtitle="Tierra y Mar"
          icon={<IconGlobe />}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 flex-1">
        <div className="lg:col-span-4 p-8 rounded-xl bg-slate-900/40 border border-slate-800 shadow-sm h-full">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2 bg-slate-800 rounded-lg text-slate-300">
              <IconBarChart />
            </div>
            <h2 className="text-lg font-semibold text-slate-200">
              Análisis de Cobertura
            </h2>
          </div>
          <div className="space-y-6">
            {Object.entries(report.estadisticas.desglose_porcentajes).sort(([,a], [,b]) => Number(b) - Number(a)).map(([key, value]) => (
              <div key={key}>
                <div className="flex justify-between mb-2 text-xs font-semibold text-slate-400">
                  <span className="uppercase tracking-widest">{key.replace(/_/g, ' ')}</span>
                  <span className="text-slate-200">{Number(value).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div 
                    className={`h-1.5 rounded-full transition-all duration-1000 ${key === 'TORMENTA' ? 'bg-red-500' : key === 'MAR' ? 'bg-blue-500' : key === 'CIRROS' ? 'bg-cyan-400' : 'bg-slate-500'}`} 
                    style={{ width: `${value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {report?.imagenes && report.imagenes.comparacion ? (
          <div className="lg:col-span-8 p-8 rounded-xl bg-slate-900/40 border border-slate-800 shadow-sm flex flex-col h-full relative">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
               <div className="flex items-center gap-3">
                 <div className="p-2 bg-slate-800 rounded-lg text-slate-300">
                   {activeTab === 'comparacion' ? <IconImage /> : <IconThermometer />}
                 </div>
                 <h2 className="text-lg font-semibold text-slate-200">
                   Visor Satelital Analítico
                 </h2>
               </div>
               
               <div className="flex flex-wrap items-center gap-4">
                 {report.boletin_pdf && (
                   <a 
                     href={`http://127.0.0.1:8000/static/${report.boletin_pdf}`} 
                     download 
                     target="_blank"
                     className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-md border border-slate-700 transition-all shadow-sm flex items-center gap-2"
                   >
                     <IconDownload />
                     PDF
                   </a>
                 )}
                 <div className="flex gap-2 p-1 bg-slate-950 rounded-lg border border-slate-800">
                   <button 
                     onClick={() => setActiveTab('comparacion')}
                     className={`px-4 py-1.5 text-xs font-semibold rounded-md transition-all ${activeTab === 'comparacion' ? 'bg-slate-800 text-cyan-400' : 'text-slate-500 hover:text-slate-300'}`}
                   >
                     Comparación ML
                   </button>
                   <button 
                     onClick={() => setActiveTab('heatmap')}
                     className={`px-4 py-1.5 text-xs font-semibold rounded-md transition-all ${activeTab === 'heatmap' ? 'bg-slate-800 text-orange-400' : 'text-slate-500 hover:text-slate-300'}`}
                   >
                     Mapa de Calor
                   </button>
                 </div>
               </div>
            </div>
            
            <div className="w-full h-[450px] bg-slate-950 rounded-lg border border-slate-800 overflow-hidden flex items-center justify-center p-2">
              <img 
                src={activeTab === 'comparacion' 
                  ? `http://127.0.0.1:8000/static/${report.imagenes.comparacion}`
                  : `http://127.0.0.1:8000/static/${report.imagenes.heatmap}`
                } 
                alt="Visor satelital" 
                className="w-full h-full object-contain"
              />
            </div>
          </div>
        ) : (
          <div className="lg:col-span-8 p-8 rounded-xl bg-slate-900/40 border border-slate-800 shadow-sm flex items-center justify-center h-full min-h-[400px]">
             <p className="text-slate-500 text-sm font-medium">Ejecute el análisis para visualizar el renderizado.</p>
          </div>
        )}
      </div>
      
      <footer className="mt-12 text-center text-xs text-slate-600 font-medium tracking-wide">
        SISTEMA VISIONMETEOR V11.0 — {new Date(report.fecha).toLocaleString()}
      </footer>
    </main>
    </div>
  );
}
