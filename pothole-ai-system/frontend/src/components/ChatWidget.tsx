import { useState, useRef, useEffect } from "react"
import { sendChatMessage } from "../services/api"

interface Message {
  role: "user" | "bot"
  text: string
}

export function ChatWidget() {
  const [open, setOpen]       = useState(false)
  const [input, setInput]     = useState("")
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", text: "Hi! I'm your StreetSafe assistant. Ask me about potholes on any Toronto street." }
  ])
  const bottomRef = useRef<HTMLDivElement>(null)

  // Auto scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  async function handleSend() {
    if (!input.trim() || loading) return

    const userMsg: Message = { role: "user", text: input }
    setMessages(prev => [...prev, userMsg])
    setInput("")
    setLoading(true)

    try {
      const data = await sendChatMessage(input)
      setMessages(prev => [...prev, { role: "bot", text: data.answer }])
    } catch {
      setMessages(prev => [...prev, {
        role: "bot",
        text: "Sorry, I couldn't reach the server. Make sure the backend is running."
      }])
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      {/* Floating button */}
      <button
        type="button"
        onClick={() => setOpen(v => !v)}
        className="fixed bottom-5 right-5 z-40 flex items-center gap-2 rounded-full bg-white/80 px-4 py-2 text-xs font-semibold text-slate-900 shadow-lg backdrop-blur-md hover:bg-white"
      >
        <span className="inline-block h-2 w-2 rounded-full bg-emerald-500" />
        <span>{open ? "Close Chat" : "Chat with StreetSafe"}</span>
      </button>

      {/* Chat window */}
      {open && (
        <div className="fixed bottom-20 right-5 z-30 w-80 rounded-3xl border border-white/20 bg-slate-900/90 shadow-2xl backdrop-blur-xl flex flex-col"
          style={{ height: "420px" }}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
            <div>
              <p className="text-sm font-semibold text-white">StreetSafe Assistant</p>
              <p className="text-[10px] text-slate-400">Ask about Toronto road safety</p>
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="rounded-full bg-white/10 px-2 py-1 text-[10px] text-slate-200 hover:bg-white/20"
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-3 py-3 flex flex-col gap-2">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`max-w-[85%] rounded-2xl px-3 py-2 text-xs leading-relaxed ${
                  msg.role === "user"
                    ? "self-end bg-emerald-500 text-slate-950"
                    : "self-start bg-slate-800/80 text-slate-100"
                }`}
              >
                {msg.text}
              </div>
            ))}
            {loading && (
              <div className="self-start bg-slate-800/80 text-slate-400 rounded-2xl px-3 py-2 text-xs">
                Thinking...
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t border-white/10 px-3 py-2 flex gap-2">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about a Toronto road..."
              className="flex-1 rounded-xl bg-slate-800/80 px-3 py-2 text-xs text-slate-100 placeholder:text-slate-500 outline-none"
            />
            <button
              type="button"
              onClick={handleSend}
              disabled={loading}
              className="rounded-xl bg-emerald-500 px-3 py-2 text-xs font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  )
}