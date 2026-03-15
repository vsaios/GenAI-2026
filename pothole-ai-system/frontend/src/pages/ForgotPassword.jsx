import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "@/context/AuthContext"
import { resetPasswordForEmail } from "@/lib/auth"

export function ForgotPassword() {
  const { user, loading } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  if (loading) {
    return (
      <main className="mx-auto flex max-w-md flex-col gap-6 px-4 py-16">
        <p className="text-slate-400">Loading…</p>
      </main>
    )
  }

  if (user) {
    navigate("/dashboard", { replace: true })
    return null
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setSuccess(false)
    setSubmitting(true)
    try {
      await resetPasswordForEmail(email)
      setSuccess(true)
    } catch (err) {
      setError(err.message || "Failed to send reset email")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="mx-auto flex max-w-md flex-col gap-6 px-4 py-16">
      <h2 className="text-2xl font-semibold tracking-tight">Forgot password?</h2>
      <p className="text-sm text-slate-400">
        Enter your email and we’ll send you a link to reset your password.
      </p>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label htmlFor="forgot-email" className="mb-1 block text-sm font-medium text-slate-200">
            Email
          </label>
          <input
            id="forgot-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
            className="w-full rounded border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100"
          />
        </div>
        {error && (
          <p className="rounded bg-red-500/10 px-3 py-2 text-sm text-red-300">{error}</p>
        )}
        {success && (
          <p className="rounded bg-emerald-500/10 px-3 py-2 text-sm text-emerald-300">
            Check your email for the reset link.
          </p>
        )}
        <button
          type="submit"
          disabled={submitting}
          className="rounded-lg bg-emerald-600 px-4 py-2.5 font-semibold text-white hover:bg-emerald-500 disabled:opacity-50"
        >
          {submitting ? "Sending…" : "Send reset link"}
        </button>
      </form>
      <p className="text-sm text-slate-400">
        <Link to="/login" className="text-emerald-400 hover:underline">
          Back to login
        </Link>
      </p>
    </main>
  )
}
