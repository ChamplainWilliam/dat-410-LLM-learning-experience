export default function LoadingDots() {
  return (
    <div className="flex justify-start mb-3">
      <div className="px-5 py-3 rounded-[14px_14px_14px_4px] bg-[#1e2230] border border-[#2a2e3d] flex gap-1.5 items-center">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-[7px] h-[7px] rounded-full bg-blue-400 animate-bounce"
            style={{ animationDelay: `${i * 0.15}s`, animationDuration: "0.8s" }}
          />
        ))}
      </div>
    </div>
  );
}
