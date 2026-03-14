import { Globe } from "@/components/ui/globe"
import { torontoReports } from "@/mock/torontoReports"

export function GlobeBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 -z-10 flex items-center justify-center">
      <div className="relative h-screen w-screen">
        <Globe reports={torontoReports} />
      </div>
    </div>
  )
}

