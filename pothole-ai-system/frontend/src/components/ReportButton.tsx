type ReportButtonProps = {
  onClick: () => void
}

export function ReportButton({ onClick }: ReportButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="rounded-full bg-red-500 px-6 py-2.5 text-sm font-semibold text-slate-50 shadow-lg hover:bg-red-400"
    >
      Report Incident
    </button>
  )
}

