import MessageContent from "./MessageContent";

export default function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div
        className={`max-w-[80%] px-4 py-2.5 text-sm leading-relaxed ${
          isUser
            ? "bg-[#1e3a5f] border border-blue-500/25 rounded-[14px_14px_4px_14px]"
            : "bg-[#1e2230] border border-[#2a2e3d] rounded-[14px_14px_14px_4px]"
        }`}
      >
        {isUser ? (
          <span className="text-slate-200">{message.content}</span>
        ) : (
          <MessageContent text={message.content} />
        )}
      </div>
    </div>
  );
}
