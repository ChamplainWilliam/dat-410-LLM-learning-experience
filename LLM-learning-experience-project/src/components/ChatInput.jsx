import { useRef, useEffect } from "react";

export default function ChatInput({ input, setInput, onSend, loading }) {
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  const canSend = input.trim() && !loading;

  return (
    <div className="px-5 py-3 pb-4 border-t border-[#2a2e3d] bg-[#1a1d27] shrink-0">
      <div className="flex gap-2.5 items-end">
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about courses, prerequisites, scheduling..."
          rows={1}
          className="flex-1 px-4 py-2.5 rounded-xl border border-[#2a2e3d] bg-[#0f1117] text-slate-200 text-sm resize-none outline-none leading-relaxed max-h-[120px] transition-colors duration-200 focus:border-blue-400 placeholder:text-slate-500"
        />
        <button
          onClick={onSend}
          disabled={!canSend}
          className={`px-5 py-2.5 rounded-xl border-none text-sm font-bold whitespace-nowrap transition-all duration-200 cursor-pointer ${
            canSend
              ? "bg-gradient-to-br from-blue-400 to-sky-400 text-white hover:opacity-90"
              : "bg-[#242836] text-slate-500 cursor-default"
          }`}
        >
          Send →
        </button>
      </div>
      <p className="text-[10.5px] text-slate-500 mt-2 text-center">
        ChamplainGuide is an AI assistant. Always verify course info with your
        official academic advisor and the registrar.
      </p>
    </div>
  );
}
