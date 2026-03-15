import { Routes, Route, Navigate, useLocation } from "react-router-dom"
import { Navbar } from "@/components/Navbar"
import { ChatWidget } from "@/components/ChatWidget"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { ReportsProvider } from "@/context/ReportsContext"
import { Landing } from "@/pages/Landing"
import { Dashboard } from "@/pages/Dashboard"
import { TorontoPage } from "@/pages/TorontoPage"
import { Report } from "@/pages/Report"
import { Login } from "@/pages/Login"
import { Signup } from "@/pages/Signup"
import { ForgotPassword } from "@/pages/ForgotPassword"

function AppContent() {
  const location = useLocation()
  const showChat =
    location.pathname === "/dashboard" ||
    location.pathname === "/toronto" ||
    location.pathname === "/report"

  return (
    <>
      <Routes>
        {/* First landing page is /home (public); then login/signup → dashboard/toronto */}
        <Route path="/" element={<Navigate to="/home" replace />} />
        <Route path="/home" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/toronto"
          element={
            <ProtectedRoute>
              <TorontoPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/report"
          element={
            <ProtectedRoute>
              <Report />
            </ProtectedRoute>
          }
        />
      </Routes>

      {showChat && <ChatWidget />}
    </>
  )
}

function App() {
  return (
    <ReportsProvider>
      <div className="min-h-screen bg-slate-950 text-slate-50">
        <Navbar />
        <AppContent />
      </div>
    </ReportsProvider>
  )
}

export default App
