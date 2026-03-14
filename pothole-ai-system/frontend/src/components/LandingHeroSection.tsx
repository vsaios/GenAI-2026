import { Map3D } from "@/components/Map3D"

export function LandingHeroSection() {
  return (
    <section className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-10 md:flex-row md:items-center">
      <div className="flex-1 space-y-4">
        <h1 className="bg-gradient-to-b from-slate-50 to-slate-400 bg-clip-text text-4xl font-bold tracking-tight text-transparent md:text-5xl lg:text-6xl">
          StreetSafe
        </h1>
        <p className="max-w-xl text-sm text-slate-300">
          AI-powered infrastructure monitoring that detects, maps, and prioritises potholes and
          road hazards in real time.
        </p>
        <p className="text-xs text-slate-400">
          Connect edge AI cameras, community reports, and city dashboards into a single live view
          of road safety.
        </p>
      </div>
      <div className="flex-1">
        <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-950/80 shadow-xl">
          <Map3D heightClass="h-[320px] md:h-[400px] lg:h-[440px]" />
        </div>
      </div>
    </section>
  )
}

