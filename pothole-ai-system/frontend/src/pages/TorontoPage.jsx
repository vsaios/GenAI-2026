import { Link } from "react-router-dom"
import { Mapbox3DMap } from "@/components/Mapbox3DMap"
import { useReports } from "@/context/ReportsContext"

export function TorontoPage() {
  const { reports, loading, error } = useReports()

  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-8">
      <section className="flex items-start justify-between gap-4">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tight">Toronto incident map</h2>
          <p className="text-sm text-slate-300">
            Explore reported issues across Downtown, North York, Scarborough, Etobicoke, and East
            York. User-submitted reports appear as blue dots.
          </p>
          {error && (
            <p className="text-xs text-amber-400">
              Could not load reports from API: {error}
            </p>
          )}
          {loading && (
            <p className="text-xs text-slate-400">Loading pothole data...</p>
          )}
        </div>
        <Link
          to="/report"
          className="shrink-0 rounded-lg bg-emerald-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-emerald-500"
        >
          Report incident
        </Link>
      </section>
      <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-3">
        <Mapbox3DMap
          reports={reports}
          userReportIds={reports.map((r) => r.id)}
          heightClass="h-[480px]"
          center={[-79.3832, 43.6532]}
          zoom={14.5}
          minZoom={13.5}
          streetLevelMode
        />
      </section>
    </main>
  )
}