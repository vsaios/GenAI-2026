export function HeroSection({ onFocusToronto }) {
  return (
    <section className="grid items-center gap-8 md:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)]">
      <div className="space-y-4">
        <h2 className="text-3xl font-semibold tracking-tight md:text-4xl">
          Global safety signals at a glance
        </h2>
        <p className="max-w-xl text-sm text-slate-300">
          StreetSafe aggregates reports from edge cameras and community members to
          highlight hotspots of potholes, unsafe intersections, broken streetlights, and
          other hazards before they become serious incidents.
        </p>
        <button
          onClick={onFocusToronto}
          className="mt-2 rounded bg-emerald-500 px-4 py-2 text-sm font-medium text-slate-950 hover:bg-emerald-400"
        >
          Focus on Toronto
        </button>
        <p className="text-xs text-slate-400">
          Tip: click or drag the globe toward Toronto to explore the region, then switch
          into the Toronto dashboard view.
        </p>
      </div>
      {/* Right column is reserved for Globe, injected by parent */}
    </section>
  )
}

