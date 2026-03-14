import { motion } from "framer-motion"

type HeroIntroProps = {
  onComplete: () => void
}

export function HeroIntro({ onComplete }: HeroIntroProps) {
  return (
    <motion.div
      className="pointer-events-none absolute inset-0 z-20 flex items-center justify-center bg-slate-950"
      initial={{ opacity: 1, y: 0, scale: 1 }}
      animate={{
        opacity: [1, 0.9, 0],
        y: [0, -30, -60],
        scale: [1, 1.01, 1.03],
      }}
      transition={{
        duration: 1,
        times: [0, 0.6, 1],
        ease: "easeOut",
      }}
      onAnimationComplete={onComplete}
    >
      <div className="text-center">
        <p className="text-xs tracking-[0.3em] text-slate-400">STREETSAFE</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-50 md:text-5xl">
          City Risk Intelligence
        </h1>
        <p className="mt-3 text-sm text-slate-400">
          Visualising community incidents and AI-detected hazards in real time.
        </p>
      </div>
    </motion.div>
  )
}

