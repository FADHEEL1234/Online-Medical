import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Register from './pages/Register'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Doctors from './pages/Doctors'
import MyAppointments from './pages/MyAppointments'
import BookAppointment from './pages/BookAppointment'
import AdminDashboard from './pages/AdminDashboard'
import './App.css'

function App() {
  const isAuthenticated = () => {
    return localStorage.getItem('token') !== null
  }

  const ProtectedRoute = ({ children }) => {
    if (!isAuthenticated()) {
      return <Navigate to="/login" replace />
    }
    return children
  }

  const ProtectedAdminRoute = ({ children }) => {
    if (!isAuthenticated() || localStorage.getItem('is_staff') !== 'true') {
      // non‑staff users get redirected to regular dashboard or login
      return <Navigate to="/dashboard" replace />
    }
    return children;
  }

  return (
    <div className="app">
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route
            path="/admin"
            element={
              <ProtectedAdminRoute>
                <AdminDashboard />
              </ProtectedAdminRoute>
            }
          />
          <Route 
            path="/doctors" 
            element={
              <ProtectedRoute>
                <Doctors />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/my-appointments" 
            element={
              <ProtectedRoute>
                <MyAppointments />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/book-appointment" 
            element={
              <ProtectedRoute>
                <BookAppointment />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </div>
    </div>
  )
}

export default App
