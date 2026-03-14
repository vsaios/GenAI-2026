import { cn } from "@/lib/utils"
import { Globe } from "@/components/ui/globe"
import { torontoReports } from "@/mock/torontoReports"

type Map3DProps = {
  heightClass?: string
  className?: string
}

/**
 * COBE 3D globe for the Home page only. Dashboard and Toronto use Mapbox3DMap.
 */
export function Map3D({ heightClass = "h-[320px]", className }: Map3DProps) {
  return (
    <div className={cn("relative w-full", heightClass, className)}>
      <Globe
        className="mx-auto max-w-full md:!max-w-[520px]"
        reports={torontoReports}
        configOverride={{
          baseColor: [0.08, 0.1, 0.14],
          markerColor: [0.4, 0.85, 1],
          glowColor: [0.5, 0.8, 1],
          dark: 1,
          diffuse: 0.35,
          mapBrightness: 1.15,
        }}
      />
    </div>
  )
}

