import { useEffect, useMemo, useRef, useState } from "react"
import mapboxgl, { Map } from "mapbox-gl"

import { torontoReports } from "@/mock/torontoReports"
import type { Report } from "@/types/report"

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || ""

type SelectedReport = Report | null

const center: [number, number] = [-79.3832, 43.6532]

function buildGeoJson(reports: Report) {
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
        issue_type: report.issue_type,
        severity: report.severity,
        timestamp: report.timestamp,
        status: report.status,
      },
    })),
  } as const
}

export function TorontoMap() {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<Map | null>(null)
  const [selected, setSelected] = useState<SelectedReport>(null)
  const [error, setError] = useState<string | null>(null)

  const geoJson = useMemo(() => buildGeoJson(torontoReports), [])

  useEffect(() => {
    if (!MAPBOX_TOKEN) {
      console.warn("Mapbox token missing. Running in demo mode.")
      setError(
        "Map disabled in demo mode — no Mapbox token provided.",
      )
      return
    }

    if (!containerRef.current) return

    mapboxgl.accessToken = MAPBOX_TOKEN

    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: "mapbox://styles/mapbox/dark-v11",
      center,
      zoom: 10,
      maxZoom: 18,
      minZoom: 3,
    })

    mapRef.current = map

    map.on("load", () => {
      map.addSource("reports", {
        type: "geojson",
        data: geoJson,
      })

      // Heatmap layer
      map.addLayer({
        id: "reports-heat",
        type: "heatmap",
        source: "reports",
        maxzoom: 15,
        paint: {
          "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["get", "severity"],
            0,
            0,
            2,
            1,
          ],
          "heatmap-intensity": [
            "interpolate",
            ["linear"],
            ["zoom"],
            6,
            0.5,
            15,
            1.5,
          ],
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0,
            "rgba(0, 0, 255, 0)",
            0.2,
            "rgba(0, 0, 255, 0.6)",
            0.4,
            "rgba(255, 255, 0, 0.6)",
            0.7,
            "rgba(255, 165, 0, 0.8)",
            1,
            "rgba(255, 0, 0, 0.9)",
          ],
          "heatmap-radius": [
            "interpolate",
            ["linear"],
            ["zoom"],
            6,
            20,
            15,
            50,
          ],
          "heatmap-opacity": 0.9,
        },
      })

      // Circle markers on top of heatmap
      map.addLayer({
        id: "reports-circle",
        type: "circle",
        source: "reports",
        minzoom: 8,
        paint: {
          "circle-radius": [
            "interpolate",
            ["linear"],
            ["zoom"],
            8,
            4,
            15,
            10,
          ],
          "circle-color": [
            "match",
            ["get", "severity"],
            "low",
            "#22c55e",
            "medium",
            "#eab308",
            "high",
            "#ef4444",
            "#64748b",
          ],
          "circle-opacity": 0.9,
          "circle-stroke-width": 1,
          "circle-stroke-color": "#020617",
        },
      })

      map.on("click", "reports-circle", (e) => {
        const feature = e.features?.[0]
        if (!feature) return
        const id = feature.properties?.id as string | undefined
        const report = torontoReports.find((r) => r.id === id)
        if (report) {
          setSelected(report)
        }
      })

      map.on("mouseenter", "reports-circle", () => {
        map.getCanvas().style.cursor = "pointer"
      })
      map.on("mouseleave", "reports-circle", () => {
        map.getCanvas().style.cursor = ""
      })
    })

    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [geoJson])

  return (
    <div className="flex flex-col gap-3">
      {MAPBOX_TOKEN ? (
        <div
          ref={containerRef}
          className="h-[420px] w-full overflow-hidden rounded-lg border border-slate-800"
        />
      ) : (
        <div className="flex h-[420px] w-full items-center justify-center rounded-lg border border-dashed border-slate-700 bg-slate-900 text-xs text-slate-400">
          Map disabled in demo mode — no Mapbox token provided.
        </div>
      )}
      {error && MAPBOX_TOKEN && (
        <p className="text-xs text-red-400">
          {error}
        </p>
      )}
      {selected && (
        <div className="space-y-1 rounded-md border border-slate-800 bg-slate-900/80 p-3 text-xs">
          <div className="flex items-center justify-between">
            <span className="font-semibold capitalize">
              {selected.issue_type.replace("-", " ")}
            </span>
            <span
              className={`rounded-full px-2 py-0.5 text-[10px] font-medium uppercase ${
                selected.severity === "high"
                  ? "bg-red-500/20 text-red-300"
                  : selected.severity === "medium"
                    ? "bg-yellow-500/20 text-yellow-300"
                    : "bg-emerald-500/20 text-emerald-300"
              }`}
            >
              {selected.severity}
            </span>
          </div>
          <p className="text-slate-300">
            Status:{" "}
            <span className="capitalize">{selected.status.replace("_", " ")}</span>
          </p>
          <p className="text-slate-400">
            Timestamp: {new Date(selected.timestamp).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  )
}

