import { Mapbox3DMap } from "@/components/Mapbox3DMap"

export function TorontoPage() {
  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-8">
      <section className="space-y-1">
        <h2 className="text-2xl font-semibold tracking-tight">Toronto incident map</h2>
        <p className="text-sm text-slate-300">
          Explore reported issues across Downtown, North York, Scarborough, Etobicoke, and East
          York. Heatmap intensity reflects repeated reports.
        </p>
      </section>
      <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-3">
        <Mapbox3DMap
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

