import { useState } from "react";
import { SYSTEM_PROMPT } from "../config/systemPrompt";
import { SUBJECT_PROMPT } from "../config/subjectPrompt";

const TABS = [
  { key: "system", label: "System Prompt", description: "Defines behavior, tone & rules (constant across subjects)" },
  { key: "subject", label: "Subject Prompt (Configurable)", description: "Subject-specific knowledge (swap for different programs)" },
];

export default function PromptConfigPanel() {
  const [activeTab, setActiveTab] = useState("system");

  return (
    <div className="border-b border-[#2a2e3d] bg-[#1a1d27]">
      {/* Tab bar */}
      <div className="flex border-b border-[#2a2e3d]">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`flex-1 py-2.5 px-4 text-xs font-semibold transition-all duration-200 border-b-2 cursor-pointer ${
              activeTab === tab.key
                ? "bg-[#242836] border-blue-400 text-blue-400"
                : "bg-transparent border-transparent text-slate-400 hover:text-slate-300"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="p-4 max-h-[220px] overflow-auto">
        <div className="text-[11px] text-slate-500 mb-2 font-semibold uppercase tracking-wide">
          {TABS.find((t) => t.key === activeTab)?.description}
        </div>
        <pre className="text-xs leading-relaxed text-slate-400 whitespace-pre-wrap font-mono m-0 bg-[#0f1117] p-3.5 rounded-lg border border-[#2a2e3d] max-h-[160px] overflow-auto">
          {activeTab === "system" ? SYSTEM_PROMPT : SUBJECT_PROMPT}
        </pre>
      </div>
    </div>
  );
}
