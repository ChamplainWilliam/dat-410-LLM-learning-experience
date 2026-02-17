export default function Header({ showConfig, onToggleConfig, onClear }) {
  return (
    <div className="px-5 py-3 border-b border-[#2a2e3d] flex items-center justify-between bg-[#1a1d27] shrink-0">
      {/* Logo + title */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-[10px] bg-gradient-to-br from-blue-400 to-sky-400 flex items-center justify-center text-lg font-bold text-white tracking-tighter">
          CG
        </div>
        <div>
          <div className="font-bold text-[15px] text-slate-200 tracking-tight">
            ChamplainGuide
          </div>
          <div className="text-[11px] text-slate-400">
            24/7 Course Scheduling Counselor • CS & Cybersecurity
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2">
        <button
          onClick={onToggleConfig}
          className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer border ${
            showConfig
              ? "border-blue-400 bg-blue-500/10 text-blue-400"
              : "border-[#2a2e3d] bg-transparent text-slate-400 hover:text-slate-300 hover:border-slate-500"
          }`}
        >
          ⚙ Prompts
        </button>
        <button
          onClick={onClear}
          className="px-3.5 py-1.5 rounded-lg border border-[#2a2e3d] bg-transparent text-slate-400 text-xs font-semibold transition-all duration-200 hover:text-slate-300 hover:border-slate-500 cursor-pointer"
        >
          ↻ Clear
        </button>
      </div>
    </div>
  );
}
