import { useState } from "react"

export function ChatWidget() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="fixed bottom-5 right-5 z-40 rounded-full bg-emerald-500 px-4 py-3 text-sm font-semibold text-slate-950 shadow-lg hover:bg-emerald-400"
      >
        {open ? "Close Chat" : "Chat with StreetSafe"}
      </button>

      {open && (
        <div className="fixed bottom-20 right-5 z-30 w-80 rounded-lg border border-slate-800 bg-slate-950/95 shadow-xl backdrop-blur">
          <div className="flex items-center justify-between border-b border-slate-800 px-3 py-2">
            <div>
              <p className="text-sm font-semibold">StreetSafe Assistant</p>
              <p className="text-[11px] text-slate-400">
                Ask about incidents, hotspots, or follow-ups.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="rounded px-2 py-1 text-[11px] text-slate-400 hover:bg-slate-800"
            >
              ×
            </button>
          </div>
          <div className="flex max-h-64 flex-col gap-2 overflow-y-auto px-3 py-2 text-xs text-slate-200">
            <div className="self-start rounded-md bg-slate-800 px-2 py-1">
              Hi! I&apos;m your StreetSafe assistant. This is a demo UI — no messages are
              sent yet.
            </div>
            <div className="self-start rounded-md bg-slate-800 px-2 py-1">
              After login, this space can summarize hotspots, explain escalation, or help you
              triage new incidents.
            </div>
          </div>
          <div className="border-t border-slate-800 px-3 py-2">
            <input
              disabled
              className="w-full rounded-md border border-slate-700 bg-slate-900 px-2 py-1 text-xs text-slate-300 placeholder:text-slate-500"
              placeholder="Chat is coming soon — demo only."
            />
          </div>
        </div>
      )}
    </>
  )
}

