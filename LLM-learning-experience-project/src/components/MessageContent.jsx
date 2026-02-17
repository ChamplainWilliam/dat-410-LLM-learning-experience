export default function MessageContent({ text }) {
  const lines = text.split("\n");

  return (
    <div className="text-slate-200">
      {lines.map((line, i) => {
        // Highlight course codes inline
        const formatLine = (str) => {
          const parts = str.split(/(\b(?:CSI|SEC|MAT)-\d{3}\b)/g);
          return parts.map((part, j) => {
            if (/^(CSI|SEC|MAT)-\d{3}$/.test(part)) {
              return (
                <span
                  key={j}
                  className="bg-[#1e3a5f] px-1.5 rounded font-mono text-xs text-sky-400"
                >
                  {part}
                </span>
              );
            }
            // Bold text
            const boldParts = part.split(/(\*\*.*?\*\*)/g);
            return boldParts.map((bp, k) => {
              if (bp.startsWith("**") && bp.endsWith("**")) {
                return (
                  <strong key={`${j}-${k}`} className="text-blue-400 font-semibold">
                    {bp.slice(2, -2)}
                  </strong>
                );
              }
              return <span key={`${j}-${k}`}>{bp}</span>;
            });
          });
        };

        // Bullet points
        if (line.startsWith("- ") || line.startsWith("• ")) {
          return (
            <div key={i} className="pl-4 relative mb-1">
              <span className="absolute left-0 text-blue-400">•</span>
              {formatLine(line.slice(2))}
            </div>
          );
        }

        // Numbered lists
        const numMatch = line.match(/^(\d+)\.\s/);
        if (numMatch) {
          return (
            <div key={i} className="pl-6 relative mb-1">
              <span className="absolute left-0 text-blue-400 font-semibold w-5 text-right">
                {numMatch[1]}.
              </span>
              {formatLine(line.slice(numMatch[0].length))}
            </div>
          );
        }

        // Empty line = spacer
        if (line.trim() === "") return <div key={i} className="h-2" />;

        // Regular paragraph
        return (
          <div key={i} className="mb-1">
            {formatLine(line)}
          </div>
        );
      })}
    </div>
  );
}
