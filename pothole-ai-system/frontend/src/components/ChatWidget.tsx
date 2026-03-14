import { motion } from "framer-motion"
import { useState } from "react"

export function ChatWidget() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <motion.button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="fixed bottom-5 right-5 z-40 flex items-center gap-2 rounded-full bg-white/80 px-4 py-2 text-xs font-semibold text-slate-900 shadow-lg backdrop-blur-md hover:bg-white"
        whileHover={{ scale: 1.04, y: -2 }}
        whileTap={{ scale: 0.98 }}
      >
        <span className="inline-block h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.9)]" />
        <span>Chat with StreetSafe</span>
      </motion.button>

      {open && (
        <motion.div
          className="fixed bottom-20 right-5 z-30 w-80 rounded-3xl border border-white/20 bg-slate-900/80 p-3 text-xs text-slate-100 shadow-2xl backdrop-blur-xl"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          transition={{ duration: 0.2 }}
        >
          <div className="mb-2 flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold">StreetSafe Assistant</p>
              <p className="text-[10px] text-slate-400">
                Demo-only chat UI. Responses are not yet connected.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="rounded-full bg-white/10 px-2 py-1 text-[10px] text-slate-200 hover:bg-white/20"
            >
              ×
            </button>
          </div>
          <div className="mb-2 max-h-52 space-y-2 overflow-y-auto">
            <div className="max-w-[85%] rounded-2xl bg-slate-800/80 px-3 py-2">
              Hi, I&apos;m your StreetSafe assistant. Ask me about hotspots, recent incidents, or
              escalation priorities.
            </div>
            <div className="max-w-[80%] rounded-2xl bg-slate-800/80 px-3 py-2">
              In this demo, messages stay on your device only.
            </div>
          </div>
          <div className="rounded-2xl bg-slate-900/80 px-2 py-1">
            <input
              disabled
              className="w-full bg-transparent px-1 py-1 text-[11px] text-slate-300 placeholder:text-slate-500"
              placeholder="Chat is coming soon — this is a preview."
            />
          </div>
        </motion.div>
      )}
    </>
  )
}

