import { useEffect, useMemo, useRef, useState } from "react"
import { motion } from "framer-motion"
import mapboxgl, { Map } from "mapbox-gl"

import { MAPBOX_TOKEN } from "@/config/env"
import { torontoReports } from "@/mock/torontoReports"
import { FLY_TO_EVENT } from "@/services/geocode"
import type { Report } from "@/types/report"
import { cn } from "@/lib/utils"
import { reverseGeocode } from "@/lib/geoapify"

type Mapbox3DMapProps = {
  heightClass?: string
  center?: [number, number]
  zoom?: number
  minZoom?: number
  streetLevelMode?: boolean
  reports?: Report[]
  userReportIds?: string[]
}

const token = MAPBOX_TOKEN
const defaultCenter: [number, number] = [-79.3832, 43.6532]

const MYHAL_CENTRE_ID = "myhal-centre"
const MYHAL_CENTRE_COORDINATES: [number, number] = [-79.396485, 43.660837]

function buildGeoJson(reports: Report[], includeMyhalCentre = false) {
  const features = reports.map((report) => ({
    type: "Feature" as const,
    geometry: {
      type: "Point" as const,
      coordinates: [report.longitude, report.latitude] as [number, number],
    },
    properties: {
      id: report.id,
      severity: report.severity,
      timestamp: report.timestamp,
      issue_type: report.issue_type,
    },
  }))

  if (includeMyhalCentre) {
    features.push({
      type: "Feature" as const,
      geometry: {
        type: "Point" as const,
        coordinates: MYHAL_CENTRE_COORDINATES,
      },
      properties: {
  id: MYHAL_CENTRE_ID,
  severity: "medium" as const,
  timestamp: new Date().toISOString(),
  issue_type: "pothole",
},
    })
  }

  return {
    type: "FeatureCollection" as const,
    features,
  }
}

function generateReportCardHtml(opts: {
  timeReported: string
  location: string
  description: string
  severityLabel: string
  badgeBg: string
  badgeColor: string
}) {
  const { timeReported, location, description, severityLabel, badgeBg, badgeColor } = opts
  return `
    <div class="popup-card" style="
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      width: 260px;
      max-width: 100%;
      background: #fff;
      color: #0f172a;
      border-radius: 12px;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
      padding: 1rem;
    ">
      <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 0.5rem 0; color: #0f172a;">Pothole Report</h3>
      <p style="margin: 0.25rem 0; font-size: 0.875rem;"><strong>Location:</strong> ${escapeHtml(location)}</p>
      <p style="margin: 0.25rem 0; font-size: 0.875rem;"><strong>Reported:</strong> ${escapeHtml(timeReported)}</p>
      <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem; color: #334155;">${escapeHtml(description)}</p>
      <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;"><strong>Severity:</strong> <span style="display: inline-block; padding: 0.2rem 0.5rem; border-radius: 9999px; background: ${badgeBg}; color: ${badgeColor}; font-weight: 500;">${escapeHtml(severityLabel)}</span></p>
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
  reports: reportsProp,
  userReportIds = [],
}: Mapbox3DMapProps) {
  const [fallbackReportId, setFallbackReportId] = useState<string | null>(null)

  const containerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<Map | null>(null)
  const popupRef = useRef<mapboxgl.Popup | null>(null)
  const clusterAnimationFrameRef = useRef<number | null>(null)

  const reports = reportsProp ?? torontoReports
  const geoJson = useMemo(
    () => buildGeoJson(reports, streetLevelMode),
    [reports, streetLevelMode],
  )

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

    const onFlyTo = (e: CustomEvent<{ lng: number; lat: number }>) => {
      if (mapRef.current) {
        mapRef.current.flyTo({
          center: [e.detail.lng, e.detail.lat],
          zoom: 15,
          essential: true,
        })
      }
    }
    window.addEventListener(FLY_TO_EVENT, onFlyTo as EventListener)

    map.on("load", () => {
      if (streetLevelMode) {
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
              "interpolate", ["linear"], ["zoom"],
              8, 5,
              15, 12,
            ],
            "circle-color": "#22d3ee",
            "circle-blur": 0.2,
            "circle-opacity": 0.95,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#0e7490",
          },
        })
      } else {
        map.addSource("incidents-clustered", {
          type: "geojson",
          data: geoJson,
          cluster: true,
          clusterRadius: 50,
          clusterMaxZoom: 14,
        })

        const clusterFilter: [string, string] = ["has", "point_count"]

        map.addLayer({
          id: "incidents-cluster-outer",
          type: "circle",
          source: "incidents-clustered",
          filter: clusterFilter,
          paint: {
            "circle-radius": [
              "interpolate", ["linear"], ["zoom"],
              8, 28,
              11, 48,
              14, 64,
            ],
            "circle-color": "rgb(34, 197, 94)",
            "circle-blur": 0.92,
            "circle-opacity": 0.26,
          },
        })

        map.addLayer({
          id: "incidents-cluster-mid",
          type: "circle",
          source: "incidents-clustered",
          filter: clusterFilter,
          paint: {
            "circle-radius": [
              "interpolate", ["linear"], ["zoom"],
              8, 16,
              11, 28,
              14, 40,
            ],
            "circle-color": "rgb(250, 204, 21)",
            "circle-blur": 0.9,
            "circle-opacity": 0.52,
          },
        })

        map.addLayer({
          id: "incidents-cluster-core",
          type: "circle",
          source: "incidents-clustered",
          filter: clusterFilter,
          paint: {
            "circle-radius": [
              "interpolate", ["linear"], ["zoom"],
              8, 10,
              11, 18,
              14, 26,
            ],
            "circle-color": "rgb(239, 68, 68)",
            "circle-blur": 0.88,
            "circle-opacity": 0.88,
          },
        })

        map.addLayer({
          id: "incidents-points",
          type: "circle",
          source: "incidents-clustered",
          filter: ["!", ["has", "point_count"]],
          paint: {
            "circle-radius": [
              "interpolate", ["linear"], ["zoom"],
              12, 4,
              15, 8,
            ],
            "circle-color": "#22d3ee",
            "circle-blur": 0.1,
            "circle-opacity": 0.95,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#0e7490",
          },
        })

        const clusterLayerIds = [
          "incidents-cluster-outer",
          "incidents-cluster-mid",
          "incidents-cluster-core",
        ]
        const baseRadii = [28, 16, 10]
        const baseOpacities = [0.26, 0.52, 0.88]

        const animateClusterGlow = () => {
          if (!map.isStyleLoaded() || !map.getLayer("incidents-cluster-outer")) {
            clusterAnimationFrameRef.current = requestAnimationFrame(animateClusterGlow)
            return
          }

          const now = performance.now()
          const t = (now % 2000) / 2000
          const pulse = 1 + 0.1 * Math.sin(t * 2 * Math.PI)
          const zoomLevel = map.getZoom()
          const zoomFactor = Math.max(0, Math.min(1, (zoomLevel - 8) / 6))

          try {
            for (let i = 0; i < clusterLayerIds.length; i++) {
              const baseR = baseRadii[i] + zoomFactor * (i === 0 ? 36 : i === 1 ? 24 : 16)
              const radius = Math.max(8, baseR * pulse)
              const baseO = baseOpacities[i]
              const opacity = baseO * (0.92 + 0.08 * Math.sin(t * 2 * Math.PI))
              map.setPaintProperty(clusterLayerIds[i], "circle-radius", radius)
              map.setPaintProperty(clusterLayerIds[i], "circle-opacity", opacity)
            }
          } catch {
            // Layers may have been removed
          }

          clusterAnimationFrameRef.current = requestAnimationFrame(animateClusterGlow)
        }

        clusterAnimationFrameRef.current = requestAnimationFrame(animateClusterGlow)

        const zoomToCluster = (e: mapboxgl.MapLayerMouseEvent) => {
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
        }

        clusterLayerIds.forEach((layerId) => {
          map.on("click", layerId, zoomToCluster)
          map.on("mouseenter", layerId, () => { map.getCanvas().style.cursor = "pointer" })
          map.on("mouseleave", layerId, () => { map.getCanvas().style.cursor = "" })
        })
      }

      // ── Cursor on individual nodes ──────────────────────────
      map.on("mouseenter", "incidents-points", () => {
        map.getCanvas().style.cursor = "pointer"
      })
      map.on("mouseleave", "incidents-points", () => {
        map.getCanvas().style.cursor = ""
      })

      // ── Click individual node → zoom in + popup ─────────────
      map.on("click", "incidents-points", async (e) => {
        e.originalEvent.stopPropagation()
        const features = e.features
        if (!features || features.length === 0) return
        const feature = features[0]

        const geom = feature.geometry as { type: string; coordinates: number[] }
        const [lng, lat] = geom.coordinates
        const coordinates: [number, number] = [lng, lat]

        // ✅ Zoom into the clicked dot
        map.flyTo({
          center: coordinates,
          zoom: Math.max(map.getZoom(), 15),
          pitch: 60,
          bearing: map.getBearing(),
          duration: 800,
          essential: true,
        })

        const id = feature.properties?.id as string | undefined
        const severity = (feature.properties?.severity as string) || "medium"
        const timestamp = feature.properties?.timestamp as string | undefined
        const issueType = (feature.properties?.issue_type as string) || "pothole"
        const isMyhal = id === MYHAL_CENTRE_ID

        const timeReported = timestamp
          ? new Date(timestamp).toLocaleString("en-CA", {
              timeZone: "America/New_York",
              dateStyle: "medium",
              timeStyle: "short",
            })
          : "Unknown"

        const description =
          issueType === "pothole"
            ? "Pothole reported in traffic lane"
            : `${issueType.replace(/-/g, " ")} reported.`

        const severityLabel =
          severity === "high" ? "High" : severity === "medium" ? "Medium" : "Low"
        const badgeBg =
          severity === "high" ? "#7f1d1d" : severity === "medium" ? "#854d0e" : "#14532d"
        const badgeColor =
          severity === "high" ? "#fca5a5" : severity === "medium" ? "#fde047" : "#86efac"

        const html = isMyhal
          ? generateReportCardHtml({
              timeReported: "1 hour ago",
              location: "Myhal Centre",
              description: "Large pothole detected near the entrance road by Myhal Centre.",
              severityLabel: "Medium",
              badgeBg: "#854d0e",
              badgeColor: "#fde047",
            })
          : generateReportCardHtml({
              timeReported,
              location: "Loading address...",
              description,
              severityLabel,
              badgeBg,
              badgeColor,
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
          offset: 25,
        })
          .setLngLat(coordinates)
          .setHTML(html)
          .addTo(map)

        popupRef.current = popup
        setFallbackReportId(null)

        if (!isMyhal) {
          reverseGeocode(lat, lng).then((address) => {
            if (popupRef.current) {
              const updatedHtml = generateReportCardHtml({
                timeReported,
                location: address,
                description,
                severityLabel,
                badgeBg,
                badgeColor,
              })
              popupRef.current.setHTML(updatedHtml)
            }
          })
        }
      })

      setTimeout(() => {
        map.resize()
      }, 100)
    })

    return () => {
      window.removeEventListener(FLY_TO_EVENT, onFlyTo as EventListener)
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
          "flex w-full items-center justify-center bg-slate-950 text-sm text-slate-400",
          heightClass,
        )}
      >
        Map loading…
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
        <div ref={containerRef} className="relative h-full w-full" />

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