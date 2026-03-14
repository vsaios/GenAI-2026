import { motion } from "framer-motion"

import { Globe } from "@/components/ui/globe"
import { torontoReports } from "@/mock/torontoReports"

export function GlobeMap() {
  return (
    <motion.div
      className="relative h-[calc(100vh-7rem)] w-full overflow-hidden bg-gradient-to-b from-slate-950 via-slate-950 to-slate-900"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
    >
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(34,197,94,0.18),transparent_55%)]" />
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_bottom,rgba(56,189,248,0.12),transparent_60%)]" />

      <div className="relative mx-auto flex h-full max-w-4xl items-center justify-center">
        <Globe
          className="top-10"
          reports={torontoReports}
          configOverride={{
            baseColor: [0.08, 0.1, 0.16],
            markerColor: [0.38, 0.82, 0.98],
            glowColor: [0.5, 0.78, 1],
            dark: 1,
            diffuse: 0.4,
            mapBrightness: 1.1,
          }}
        />
      </div>
    </motion.div>
  )
}

