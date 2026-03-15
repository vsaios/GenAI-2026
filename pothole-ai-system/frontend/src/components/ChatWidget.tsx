import { useState, useRef, useEffect } from "react"
import { MAPBOX_TOKEN } from "@/config/env"
import { sendChatMessage } from "@/services/api"
import { geocodeToToronto, emitFlyTo } from "@/services/geocode"

interface Message {
  role: "user" | "bot"
  text: string
}

function looksLikeStreetQuery(text: string): boolean {
  const streetKeywords = [
    "on ", "at ", "near ", "around ", "street", "ave", "avenue",
    "blvd", "boulevard", "road", "rd", "drive", "dr", "way",
    "lane", "crescent", "court", "place", "gardens", "park",
    "danforth", "bloor", "yonge", "queen", "king", "eglinton",
    "finch", "sheppard", "dundas", "college", "spadina", "bathurst",
    "ossington", "roncesvalles", "parliament", "woodbine", "keele",
    "allen", "davenport", "victoria"
  ]
  const lower = text.toLowerCase()
  return streetKeywords.some(kw => lower.includes(kw))
}

function extractCoordsFromResponse(text: string): { lat: number; lng: number } | null {
  const match = text.match(/\((-?\d+\.\d+),\s*(-?\d+\.\d+)\)/)
  if (match) {
    const lat = parseFloat(match[1])
    const lng = parseFloat(match[2])
    if (lat > 43.4 && lat < 44.0 && lng > -80.0 && lng < -79.0) {
      return { lat, lng }
    }
  }
  return null
}

export function ChatWidget() {
  const [open, setOpen]         = useState(false)
  const [input, setInput]       = useState("")
  const [loading, setLoading]   = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", text: "Hi! I'm your Rua assistant. Ask me about potholes on any Toronto street." }
  ])
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  async function handleSend() {
    if (!input.trim() || loading) return
    const userMsg: Message = { role: "user", text: input }
    const messageText = input
    setMessages(prev => [...prev, userMsg])
    setInput("")
    setLoading(true)

    try {
      const data = await sendChatMessage(messageText)
      setMessages(prev => [...prev, { role: "bot", text: data.answer }])

      // ✅ First try to fly to coords extracted from chatbot response
      const coords = extractCoordsFromResponse(data.answer)
      if (coords) {
        console.log("[ChatWidget] flying to pothole coords:", coords)
        emitFlyTo(coords.lng, coords.lat)
      }
      // ✅ Fallback: geocode the street name from user message
      else if (looksLikeStreetQuery(messageText)) {
        geocodeToToronto(messageText, MAPBOX_TOKEN).then((geocoded) => {
          if (geocoded) {
            console.log("[ChatWidget] flying to geocoded street:", geocoded)
            emitFlyTo(geocoded.lng, geocoded.lat)
          }
        })
      }

    } catch (err: unknown) {
      const msg = err instanceof Error
        ? err.message
        : "Sorry, I couldn't reach the server. Make sure the backend is running."
      setMessages(prev => [...prev, { role: "bot", text: msg }])
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
      <button
        type="button"
        onClick={() => setOpen(v => !v)}
        className="fixed bottom-5 right-5 z-40 flex items-center gap-2.5 rounded-full bg-white/80 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg backdrop-blur-md hover:bg-white"
      >
        <span className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-500" />
        <span>{open ? "Close Chat" : "Chat with Rua"}</span>
      </button>

      {open && (
        <div
          className="fixed bottom-24 right-5 z-30 w-80 rounded-3xl border border-white/20 bg-slate-900/90 shadow-2xl backdrop-blur-xl flex flex-col"
          style={{ height: "420px" }}
        >
          <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
            <div>
              <p className="text-sm font-semibold text-white">Rua Assistant</p>
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