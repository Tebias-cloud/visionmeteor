'use client';

const ImageIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-slate-400">
    <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
  </svg>
);

interface UploaderProps {
  visibleFile: File | null;
  irFile: File | null;
  setVisibleFile: (file: File | null) => void;
  setIrFile: (file: File | null) => void;
}

export default function Uploader({ visibleFile, irFile, setVisibleFile, setIrFile }: UploaderProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 w-full">
      {/* Input Visible */}
      <div className={`relative border border-slate-800 rounded-xl p-6 transition-all bg-black/40 backdrop-blur-md ${visibleFile ? 'border-cyan-500/50 shadow-[0_0_15px_rgba(6,182,212,0.15)]' : 'hover:border-slate-600'}`}>
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 bg-slate-900 rounded-lg">
            <ImageIcon />
          </div>
          <label className="text-sm font-semibold text-slate-200 uppercase tracking-widest">
            Espectro Visible
          </label>
        </div>
        <p className="text-xs text-slate-400 mb-4 line-clamp-1">
          {visibleFile ? `Seleccionado: ${visibleFile.name}` : 'Seleccione la imagen RGB.'}
        </p>
        <input 
          type="file" 
          accept="image/*"
          onChange={e => setVisibleFile(e.target.files?.[0] || null)}
          className="block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-cyan-950 file:text-cyan-400 hover:file:bg-cyan-900 transition-colors cursor-pointer"
        />
      </div>

      {/* Input IR */}
      <div className={`relative border border-slate-800 rounded-xl p-6 transition-all bg-black/40 backdrop-blur-md ${irFile ? 'border-orange-500/50 shadow-[0_0_15px_rgba(249,115,22,0.15)]' : 'hover:border-slate-600'}`}>
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 bg-slate-900 rounded-lg">
            <ImageIcon />
          </div>
          <label className="text-sm font-semibold text-slate-200 uppercase tracking-widest">
            Espectro Térmico (IR)
          </label>
        </div>
        <p className="text-xs text-slate-400 mb-4 line-clamp-1">
          {irFile ? `Seleccionado: ${irFile.name}` : 'Seleccione mapa falso color.'}
        </p>
        <input 
          type="file" 
          accept="image/*"
          onChange={e => setIrFile(e.target.files?.[0] || null)}
          className="block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-orange-950 file:text-orange-400 hover:file:bg-orange-900 transition-colors cursor-pointer"
        />
      </div>
    </div>
  )
}
