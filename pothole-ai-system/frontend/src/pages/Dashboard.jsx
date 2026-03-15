import { useState } from "react"
import { Link } from "react-router-dom"
import { useAuth } from "@/context/AuthContext"
import { HeroIntro } from "@/components/HeroIntro"
import { Mapbox3DMap } from "@/components/Mapbox3DMap"
import { useReports } from "@/context/ReportsContext"

export function Dashboard() {
  const { user } = useAuth()
  const [showIntro, setShowIntro] = useState(true)
  const { reports } = useReports()

  return (
    <main className="relative min-h-[calc(100vh-4rem)] bg-slate-950">
      <p className="absolute left-6 top-4 z-10 text-xs text-slate-400">
        Welcome, {user?.email ?? ""}
      </p>
      <div className="absolute right-6 top-4 z-10 flex items-center gap-3 rounded-lg border border-slate-800 bg-slate-900/90 px-3 py-2 text-sm">
        <Link
          to="/report"
          className="rounded-lg bg-emerald-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-emerald-500"
        >
          Report incident
        </Link>
      </div>
      <Mapbox3DMap
        reports={reports}
        userReportIds={reports.map((r) => r.id)}
      />
      {showIntro && <HeroIntro onComplete={() => setShowIntro(false)} />}
    </main>
  )
}