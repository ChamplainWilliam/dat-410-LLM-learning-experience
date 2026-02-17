const SUGGESTED_QUESTIONS = [
  "What courses should I take as a freshman CS major?",
  "I want to get into AI — what's the prerequisite chain?",
  "Can you help me plan my junior year schedule?",
  "What cybersecurity electives can I take?",
];

export default function WelcomeScreen({ onSelectQuestion }) {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-5 pb-10">
      {/* Icon */}
      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-400/20 to-sky-400/20 flex items-center justify-center text-3xl">
        🎓
      </div>

      {/* Title & subtitle */}
      <div className="text-center">
        <h2 className="text-lg font-bold tracking-tight text-slate-200 mb-1.5">
          Welcome to ChamplainGuide
        </h2>
        <p className="text-[13px] text-slate-400 max-w-[380px] leading-relaxed">
          I&apos;m your 24/7 academic counselor for Computer Science and
          Cybersecurity programs. Ask me about courses, prerequisites,
          scheduling, or degree planning.
        </p>
      </div>

      {/* Suggested questions grid */}
      <div className="grid grid-cols-2 gap-2 max-w-[480px] w-full">
        {SUGGESTED_QUESTIONS.map((q, i) => (
          <button
            key={i}
            onClick={() => onSelectQuestion(q)}
            className="px-3.5 py-2.5 rounded-[10px] border border-[#2a2e3d] bg-[#1a1d27] text-slate-400 text-xs text-left leading-snug transition-all duration-200 hover:border-blue-400 hover:text-slate-200 hover:bg-[#242836] cursor-pointer"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
