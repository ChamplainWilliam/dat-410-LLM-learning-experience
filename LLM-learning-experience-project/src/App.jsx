import { useState, useRef, useEffect } from "react";
import Header from "./components/Header";
import PromptConfigPanel from "./components/PromptConfigPanel";
import WelcomeScreen from "./components/WelcomeScreen";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import LoadingDots from "./components/LoadingDots";
import { SYSTEM_PROMPT } from "./config/systemPrompt";
import { SUBJECT_PROMPT } from "./config/subjectPrompt";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMsg = { role: "user", content: trimmed };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": import.meta.env.VITE_ANTHROPIC_API_KEY || "",
          "anthropic-version": "2023-06-01",
          "anthropic-dangerous-direct-browser-access": "true",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1024,
          system: SYSTEM_PROMPT + "\n\n" + SUBJECT_PROMPT,
          messages: newMessages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      const data = await response.json();
      const assistantText = data.content
        ?.map((block) => (block.type === "text" ? block.text : ""))
        .filter(Boolean)
        .join("\n");

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            assistantText ||
            "I'm sorry, I had trouble processing that. Could you try rephrasing your question?",
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I'm having trouble connecting right now. Please try again in a moment.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectQuestion = (question) => {
    setInput(question);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="h-screen flex flex-col bg-[#0f1117] text-slate-200 font-sans">
      <Header
        showConfig={showConfig}
        onToggleConfig={() => setShowConfig(!showConfig)}
        onClear={clearChat}
      />

      {showConfig && <PromptConfigPanel />}

      {/* Messages area */}
      <div className="flex-1 overflow-auto px-5 pt-5 pb-2">
        {messages.length === 0 ? (
          <WelcomeScreen onSelectQuestion={handleSelectQuestion} />
        ) : (
          <>
            {messages.map((msg, i) => (
              <ChatMessage key={i} message={msg} />
            ))}
            {loading && <LoadingDots />}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        input={input}
        setInput={setInput}
        onSend={sendMessage}
        loading={loading}
      />
    </div>
  );
}
