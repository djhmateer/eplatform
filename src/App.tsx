import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Search from './pages/Search'

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <header className="bg-white shadow-sm">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Link to="/" className="text-xl font-semibold text-slate-900 hover:text-slate-700 transition-colors">EPlatform</Link>
            <nav className="flex gap-6">
              <Link to="/search" className="text-slate-600 hover:text-slate-900 transition-colors">Search</Link>
            </nav>
          </div>
          <button className="px-4 py-2 bg-slate-900 text-white rounded-md hover:bg-slate-800 transition-colors">
            Login
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-5xl mx-auto w-full px-6 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
        </Routes>
      </main>

      <footer className="bg-white border-t border-slate-200">
        <div className="max-w-5xl mx-auto px-6 py-4 text-center text-slate-500 text-sm">
          &copy; {new Date().getFullYear()} EPlatform. All rights reserved.
        </div>
      </footer>
    </div>
  )
}

export default App
