import { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import Home from './pages/Home'
import Search from './pages/Search'
import ServerTime from './pages/ServerTime'
import Users from './pages/Users'
import Login from './pages/Login'
import Register from './pages/Register'

interface User {
  id: number
  email: string
}

function App() {
  const [user, setUser] = useState<User | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetch('/api/me', { credentials: 'include' })
      .then(res => res.ok ? res.json() : null)
      .then(data => setUser(data?.user || null))
  }, [])

  const handleLogout = async () => {
    await fetch('/api/logout', { method: 'POST', credentials: 'include' })
    setUser(null)
    navigate('/')
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <header className="bg-white shadow-sm">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Link to="/" className="text-xl font-semibold text-slate-900 hover:text-slate-700 transition-colors">EPlatform</Link>
            <nav className="flex gap-6">
              <Link to="/search" className="text-slate-600 hover:text-slate-900 transition-colors">Search</Link>
              <Link to="/servertime" className="text-slate-600 hover:text-slate-900 transition-colors">Server Time</Link>
              <Link to="/users" className="text-slate-600 hover:text-slate-900 transition-colors">Users</Link>
            </nav>
          </div>
          {user ? (
            <div className="flex items-center gap-4">
              <span className="text-slate-600">{user.email}</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-slate-900 text-white rounded-md hover:bg-slate-800 transition-colors"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login" className="px-4 py-2 bg-slate-900 text-white rounded-md hover:bg-slate-800 transition-colors">
                Login
              </Link>
              <Link to="/register" className="px-4 py-2 border border-slate-300 text-slate-700 rounded-md hover:bg-slate-100 transition-colors">
                Register
              </Link>
            </div>
          )}
        </div>
      </header>

      <main className="flex-1 max-w-5xl mx-auto w-full px-6 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/users" element={<Users />} />
          <Route path="/servertime" element={<ServerTime />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>

      <footer className="bg-white border-t border-slate-200">
        <div className="max-w-5xl mx-auto px-6 py-4 text-center text-slate-500 text-sm">
          &copy; {new Date().getFullYear()} EPlatform. 
        </div>
      </footer>
    </div>
  )
}

export default App
