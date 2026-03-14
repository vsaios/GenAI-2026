import { useState } from "react"
import { HeroIntro } from "@/components/HeroIntro"
import { Mapbox3DMap } from "@/components/Mapbox3DMap"

export function Dashboard() {
  const [showIntro, setShowIntro] = useState(true)

  return (
    <main className="relative min-h-[calc(100vh-4rem)] bg-slate-950">
      <Mapbox3DMap />
      {showIntro && <HeroIntro onComplete={() => setShowIntro(false)} />}
    </main>
  )
}
