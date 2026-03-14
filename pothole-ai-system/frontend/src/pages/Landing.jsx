import { LandingHeroSection } from "@/components/LandingHeroSection"
import { LandingFeatures } from "@/components/LandingFeatures"

export function Landing() {
  return (
    <main className="bg-slate-950">
      <LandingHeroSection />
      <LandingFeatures />
    </main>
  )
}

