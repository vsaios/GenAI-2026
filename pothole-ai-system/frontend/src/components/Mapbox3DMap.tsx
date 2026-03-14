import { useEffect, useMemo, useRef } from "react"
import { motion } from "framer-motion"
import mapboxgl, { Map } from "mapbox-gl"

import { torontoReports } from "@/mock/torontoReports"
import type { Report } from "@/types/report"
import { cn } from "@/lib/utils"

type Mapbox3DMapProps = {
  heightClass?: string
}

const token = import.meta.env.VITE_MAPBOX_TOKEN || ""

const center: [number, number] = [-79.3832, 43.6532]

function buildGeoJson(reports: Report[]) {
  return {
    type: "FeatureCollection",
    features: reports.map((report) => ({
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [report.longitude, report.latitude],
      },
      properties: {
        id: report.id,
        severity: report.severity,
      },
    })),
  } as const
}

export function Mapbox3DMap({ heightClass = "h-[calc(100vh-4rem)]" }: Mapbox3DMapProps) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<Map | null>(null)

  const geoJson = useMemo(() => buildGeoJson(torontoReports), [])

  useEffect(() => {
    if (!token) {
      console.warn("Mapbox token missing. Running map in demo fallback mode.")
      return
    }

    if (!containerRef.current) return

    mapboxgl.accessToken = token

    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: "mapbox://styles/mapbox/dark-v11",
      center,
      zoom: 10,
      pitch: 60,
      bearing: -20,
      antialias: true,
      maxZoom: 19,
      minZoom: 3,
    })

    mapRef.current = map

    map.on("load", () => {
      map.addSource("incidents", {
        type: "geojson",
        data: geoJson,
      })

      map.addLayer({
        id: "incidents-heat",
        type: "heatmap",
        source: "incidents",
        maxzoom: 15,
        paint: {
          "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["zoom"],
            6,
            0.3,
            15,
            1.2,
          ],
          "heatmap-intensity": [
            "interpolate",
            ["linear"],
            ["zoom"],
            6,
            0.4,
            15,
            1.4,
          ],
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0,
            "rgba(0,0,0,0)",
            0.2,
            "rgba(56,189,248,0.4)",
            0.4,
            "rgba(59,130,246,0.6)",
            0.7,
            "rgba(236,72,153,0.8)",
            1,
            "rgba(239,68,68,0.95)",
          ],
          "heatmap-radius": [
            "interpolate",
            ["linear"],
            ["zoom"],
            6,
            20,
            15,
            55,
          ],
          "heatmap-opacity": 0.85,
        },
      })

      map.addLayer({
        id: "incidents-points",
        type: "circle",
        source: "incidents",
        minzoom: 8,
        paint: {
          "circle-radius": [
            "interpolate",
            ["linear"],
            ["zoom"],
            8,
            2.5,
            15,
            6,
          ],
          "circle-color": "#22d3ee",
          "circle-blur": 0.4,
          "circle-opacity": 0.9,
          "circle-stroke-width": 0.5,
          "circle-stroke-color": "#020617",
        },
      })

      // Ensure map fills container after any layout/animation changes
      setTimeout(() => {
        map.resize()
      }, 100)
    })

    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [geoJson])

  if (!token) {
    return (
      <div
        className={cn(
          "flex w-full items-center justify-center bg-slate-950 text-xs text-slate-400",
          heightClass,
        )}
      >
        Map unavailable: missing Mapbox token. Add VITE_MAPBOX_TOKEN in a .env file to see the
        3D map.
      </div>
    )
  }

  return (
    <motion.div
      className={cn("w-full", heightClass)}
      initial={{ opacity: 0, scale: 0.99 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
    >
      <div ref={containerRef} className="h-full w-full" />
    </motion.div>
  )
}

