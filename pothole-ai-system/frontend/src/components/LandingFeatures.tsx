export function LandingFeatures() {
  return (
    <section className="mx-auto flex max-w-6xl flex-col gap-10 px-4 pb-16 pt-4">
      <div>
        <h2 className="text-xl font-semibold tracking-tight text-slate-50">How it works</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <div className="space-y-2 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-emerald-400">
              1. Detect
            </p>
            <p className="text-sm text-slate-200">
              Edge AI cameras and community reports flag potholes, flooding, and unsafe
              intersections in real time.
            </p>
          </div>
          <div className="space-y-2 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-emerald-400">
              2. Map
            </p>
            <p className="text-sm text-slate-200">
              Incidents are plotted onto a 3D city map, clustered into hotspots, and scored by
              severity and repeat frequency.
            </p>
          </div>
          <div className="space-y-2 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-emerald-400">
              3. Repair
            </p>
            <p className="text-sm text-slate-200">
              Crews receive prioritised work lists and follow-ups so the highest-risk segments are
              fixed first.
            </p>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-xl font-semibold tracking-tight text-slate-50">Why it matters</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <div className="space-y-1 text-sm text-slate-200">
            <p className="font-medium text-slate-100">Safer streets</p>
            <p className="text-slate-300">
              Fewer surprise hazards for cyclists, drivers, and pedestrians thanks to faster
              detection.
            </p>
          </div>
          <div className="space-y-1 text-sm text-slate-200">
            <p className="font-medium text-slate-100">Faster repairs</p>
            <p className="text-slate-300">
              Operations teams see exactly where repeated complaints and camera hits cluster.
            </p>
          </div>
          <div className="space-y-1 text-sm text-slate-200">
            <p className="font-medium text-slate-100">City insights</p>
            <p className="text-slate-300">
              Trendlines and hotspots help cities plan resurfacing budgets and long-term
              infrastructure upgrades.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

