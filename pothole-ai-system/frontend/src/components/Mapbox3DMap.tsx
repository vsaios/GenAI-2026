import { useEffect, useMemo, useRef, useState } from "react"
import { motion } from "framer-motion"
import mapboxgl, { Map } from "mapbox-gl"

import { torontoReports } from "@/mock/torontoReports"
import type { Report } from "@/types/report"
import { cn } from "@/lib/utils"

type Mapbox3DMapProps = {
  heightClass?: string
  center?: [number, number]
  zoom?: number
  minZoom?: number
  /** When true (Toronto map): simple individual node markers only. When false (dashboard): density-aware (cluster glow + isolated nodes). */
  streetLevelMode?: boolean
}

const token = import.meta.env.VITE_MAPBOX_TOKEN || ""

const defaultCenter: [number, number] = [-79.3832, 43.6532]

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

function generateReportCardHtml(opts: {
  timeReported: string
  location: string
  description: string
  severityLabel: string
  badgeBg: string
  badgeColor: string
}) {
  const {
    timeReported,
    location,
    description,
    severityLabel,
    badgeBg,
    badgeColor,
  } = opts
  return `
    <div style="
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      width: 260px;
      max-width: 100%;
      background: #fff;
      color: #0f172a;
      border-radius: 12px;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
      padding: 1rem;
    ">
      <div style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.5rem; color: #0f172a;">
        Pothole Report
      </div>
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <div>
          <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.125rem; text-transform: uppercase; letter-spacing: 0.05em;">Time Reported</div>
          <div style="font-size: 0.875rem; font-weight: 500; color: #0f172a;">${escapeHtml(timeReported)}</div>
        </div>
        <div>
          <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.125rem; text-transform: uppercase; letter-spacing: 0.05em;">Location</div>
          <div style="font-size: 0.875rem; font-weight: 500; color: #0f172a;">${escapeHtml(location)}</div>
        </div>
        <div>
          <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.125rem; text-transform: uppercase; letter-spacing: 0.05em;">Description</div>
          <div style="font-size: 0.875rem; font-weight: 500; color: #0f172a;">${escapeHtml(description)}</div>
        </div>
        <div>
          <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.125rem; text-transform: uppercase; letter-spacing: 0.05em;">Severity</div>
          <span style="
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 500;
            padding: 0.2rem 0.5rem;
            border-radius: 9999px;
            background: ${badgeBg};
            color: ${badgeColor};
          ">${escapeHtml(severityLabel)}</span>
        </div>
      </div>
    </div>
  `
}

function escapeHtml(s: string) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
}


export function Mapbox3DMap({
  heightClass = "h-[calc(100vh-4rem)]",
  center,
  zoom,
  minZoom,
  streetLevelMode = false,
}: Mapbox3DMapProps) {
  const [fallbackReportId, setFallbackReportId] = useState<string | null>(null)

  const containerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<Map | null>(null)
  const popupRef = useRef<mapboxgl.Popup | null>(null)
  const clusterAnimationFrameRef = useRef<number | null>(null)

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
      center: center ?? defaultCenter,
      zoom: zoom ?? 10,
      pitch: 60,
      bearing: -20,
      antialias: true,
      maxZoom: 19,
      minZoom: minZoom ?? 3,
    })

    mapRef.current = map

    map.on("load", () => {
      if (streetLevelMode) {
        // Toronto zoom map: normal individual node markers only. No heatmap, no clustering.
        map.addSource("incidents", {
          type: "geojson",
          data: geoJson,
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
              5,
              15,
              12,
            ],
            "circle-color": "#22d3ee",
            "circle-blur": 0.2,
            "circle-opacity": 0.95,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#0e7490",
          },
        })
      } else {
        // Main dashboard map: density-aware rendering.
        // Dense/overlapping areas → heat-style glow; isolated incidents → individual blue nodes.
        map.addSource("incidents-clustered", {
          type: "geojson",
          data: geoJson,
          cluster: true,
          clusterRadius: 50,
          clusterMaxZoom: 14,
        })

        // Density heatmap with green → yellow → red gradient based on cluster size.
        map.addLayer({
          id: "incidents-cluster-glow",
          type: "circle",
          source: "incidents-clustered",
          filter: ["has", "point_count"],
          paint: {
            // Base radius; we will also animate this for a subtle pulse.
            "circle-radius": [
              "interpolate",
              ["linear"],
              ["zoom"],
              8,
              18,
              11,
              30,
              14,
              42,
            ],
            "circle-color": [
              "interpolate",
              ["linear"],
              ["get", "point_count"],
              1,
              "rgba(22,163,74,0.28)",  // low: soft green
              5,
              "rgba(34,197,94,0.42)", // green
              10,
              "rgba(234,179,8,0.6)",  // yellow
              20,
              "rgba(250,204,21,0.75)", // brighter yellow
              35,
              "rgba(248,113,113,0.85)", // light red
              60,
              "rgba(239,68,68,0.9)",   // red
              100,
              "rgba(220,38,38,0.92)",  // intense red
            ],
            "circle-blur": 0.9,
            "circle-opacity": 0.8,
          },
        })

        map.addLayer({
          id: "incidents-points",
          type: "circle",
          source: "incidents-clustered",
          filter: ["!", ["has", "point_count"]],
          paint: {
            "circle-radius": [
              "interpolate",
              ["linear"],
              ["zoom"],
              12,
              4,
              15,
              8,
            ],
            "circle-color": "#22d3ee",
            "circle-blur": 0.1,
            "circle-opacity": 0.95,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#0e7490",
          },
        })

        // Subtle pulse animation for cluster glow: expand/fade and return.
        const animateClusterGlow = () => {
          if (!map.isStyleLoaded() || !map.getLayer("incidents-cluster-glow")) {
            clusterAnimationFrameRef.current = requestAnimationFrame(animateClusterGlow)
            return
          }

          const now = performance.now()
          const t = (now % 2000) / 2000 // 0 → 1 over 2s
          const pulse = 1 + 0.12 * Math.sin(t * 2 * Math.PI)
          const zoomLevel = map.getZoom()
          const baseRadius = 18 + (zoomLevel - 8) * 3
          const radius = Math.max(14, baseRadius * pulse)

          const baseOpacity = 0.65
          const opacity = baseOpacity + 0.18 * Math.sin(t * 2 * Math.PI)

          try {
            map.setPaintProperty("incidents-cluster-glow", "circle-radius", radius)
            map.setPaintProperty("incidents-cluster-glow", "circle-opacity", opacity)
          } catch {
            // Layer may have been removed; ignore and let cleanup stop the loop.
          }

          clusterAnimationFrameRef.current = requestAnimationFrame(animateClusterGlow)
        }

        clusterAnimationFrameRef.current = requestAnimationFrame(animateClusterGlow)

        // Click on a hotspot (cluster glow) to smoothly zoom into that area.
        map.on("click", "incidents-cluster-glow", (e) => {
          e.originalEvent.stopPropagation()
          const features = e.features
          if (!features || features.length === 0) return
          const feature = features[0]
          const geom = feature.geometry as { type: string; coordinates: number[] }
          const [lng, lat] = geom.coordinates

          const currentZoom = map.getZoom()
          const targetZoom = Math.min(14, Math.max(currentZoom + 2.5, 11))

          map.easeTo({
            center: [lng, lat],
            zoom: targetZoom,
            duration: 900,
            essential: true,
          })
        })
      }

      // Cursor and popup on individual incident nodes
      map.on("mouseenter", "incidents-points", () => {
        map.getCanvas().style.cursor = "pointer"
      })
      map.on("mouseleave", "incidents-points", () => {
        map.getCanvas().style.cursor = ""
      })

      map.on("click", "incidents-points", (e) => {
        e.originalEvent.stopPropagation()
        const features = e.features
        if (!features || features.length === 0) return
        const feature = features[0]

        const geom = feature.geometry as { type: string; coordinates: number[] }
        const coordinates: [number, number] = [geom.coordinates[0], geom.coordinates[1]]

        // Synthetic data for popup (per requirements)
        const html = generateReportCardHtml({
          timeReported: "March 18, 2026 – 2:14 PM",
          location: "Queen St W & Spadina Ave",
          description: "Large pothole reported in right traffic lane",
          severityLabel: "Moderate",
          badgeBg: "#854d0e",
          badgeColor: "#fde047",
        })

        if (popupRef.current) {
          popupRef.current.remove()
          popupRef.current = null
        }

        const popup = new mapboxgl.Popup({
          closeButton: true,
          closeOnClick: true,
          maxWidth: "300px",
          anchor: "bottom",
          offset: [0, -8],
        })
          .setLngLat(coordinates)
          .setHTML(html)
          .addTo(map)

        popupRef.current = popup
        setFallbackReportId(null)
      })

      setTimeout(() => {
        map.resize()
      }, 100)
    })

    return () => {
      if (clusterAnimationFrameRef.current !== null) {
        cancelAnimationFrame(clusterAnimationFrameRef.current)
        clusterAnimationFrameRef.current = null
      }
      if (popupRef.current) {
        popupRef.current.remove()
        popupRef.current = null
      }
      map.remove()
      mapRef.current = null
    }
  }, [geoJson, center, zoom, minZoom, streetLevelMode])

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
      <div className="relative h-full w-full">
        <div ref={containerRef} className="h-full w-full" />

        {fallbackReportId && (
          <div className="pointer-events-none absolute inset-y-4 right-4 z-10 flex items-start justify-end">
            <div className="pointer-events-auto w-[280px] max-w-[320px] rounded-xl bg-white p-4 text-slate-900 shadow-xl ring-1 ring-black/5 dark:bg-zinc-900 dark:text-zinc-50">
              <div className="mb-3 text-lg font-semibold">Pothole Report</div>
              <div className="space-y-3 text-xs text-slate-500 dark:text-zinc-400">
                <div>
                  <div className="mb-1 text-[11px] uppercase tracking-wide opacity-80">
                    Time Reported
                  </div>
                  <div className="text-sm font-medium text-slate-900 dark:text-zinc-100">
                    {/* Static fallback text since popup failed */}
                    March 18, 2026 – 2:14 PM
                  </div>
                </div>
                <div>
                  <div className="mb-1 text-[11px] uppercase tracking-wide opacity-80">
                    Location
                  </div>
                  <div className="text-sm font-medium text-slate-900 dark:text-zinc-100">
                    Queen St W &amp; Spadina Ave, Toronto
                  </div>
                </div>
                <div>
                  <div className="mb-1 text-[11px] uppercase tracking-wide opacity-80">
                    Description
                  </div>
                  <div className="text-sm font-medium text-slate-900 dark:text-zinc-100">
                    Large pothole reported in the right traffic lane.
                  </div>
                </div>
                <div>
                  <div className="mb-1 text-[11px] uppercase tracking-wide opacity-80">
                    Severity
                  </div>
                  <span className="inline-flex items-center rounded-full bg-amber-900 px-2 py-1 text-[11px] font-medium text-amber-200">
                    Moderate
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  )
}

