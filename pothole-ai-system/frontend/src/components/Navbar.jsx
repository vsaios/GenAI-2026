import { ReportButton } from "@/components/ReportButton"

export function Navbar({ currentPage, onNavigate }) {
  return (
    <header className="flex items-center justify-between border-b border-slate-800 px-6 py-4">
      <div className="flex items-center gap-2">
        <span className="text-xl font-semibold tracking-tight">StreetSafe</span>
        <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] uppercase text-emerald-300">
          beta
        </span>
      </div>

      <nav className="flex items-center gap-3 text-sm">
        <button
          onClick={() => onNavigate("landing")}
          className={`rounded px-3 py-1 ${
            currentPage === "landing"
              ? "bg-slate-100 text-slate-900"
              : "bg-slate-800 text-slate-100"
          }`}
        >
          Global view
        </button>
        <button
          onClick={() => onNavigate("toronto")}
          className={`rounded px-3 py-1 ${
            currentPage === "toronto"
              ? "bg-slate-100 text-slate-900"
              : "bg-slate-800 text-slate-100"
          }`}
        >
          Toronto map
        </button>
        <button
          onClick={() => onNavigate("dashboard")}
          className={`rounded px-3 py-1 ${
            currentPage === "dashboard"
              ? "bg-slate-100 text-slate-900"
              : "bg-slate-800 text-slate-100"
          }`}
        >
          Dashboard
        </button>
      </nav>

      <div className="flex items-center gap-2">
        {currentPage === "landing" ? (
          <>
            <button className="rounded-full px-4 py-1.5 text-xs font-medium text-slate-100 transition-colors hover:bg-slate-800/80">
              Login
            </button>
            <button className="rounded-full bg-slate-100 px-4 py-1.5 text-xs font-semibold text-slate-900 shadow-sm transition-colors hover:bg-white">
              Sign Up
            </button>
          </>
        ) : (
          <ReportButton onClick={() => onNavigate("report")} />
        )}
      </div>
    </header>
  )
}

