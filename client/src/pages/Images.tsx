import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function Images() {
  const [authorized, setAuthorized] = useState<boolean | null>(null)

  useEffect(() => {
    fetch('/api/me', { credentials: 'include' })
      .then(res => setAuthorized(res.ok))
  }, [])

  if (authorized === null) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">Images</h1>
        <p className="text-slate-600">Loading...</p>
      </div>
    )
  }

  if (!authorized) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">Images</h1>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">You must be logged in to view images</p>
          <Link to="/login" className="mt-2 inline-block text-red-700 underline hover:text-red-800">
            Go to Login
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Images</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <img src="/lake1.jpg" alt="Lake" className="w-full h-48 object-cover rounded mb-2" />
          <p className="text-slate-600 text-center">Lake</p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm">
          <img src="/landscape.jpg" alt="Landscape" className="w-full h-48 object-cover rounded mb-2" />
          <p className="text-slate-600 text-center">Landscape</p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm">
          <img src="/rainbow.jpg" alt="Rainbow" className="w-full h-48 object-cover rounded mb-2" />
          <p className="text-slate-600 text-center">Rainbow</p>
        </div>
      </div>
    </div>
  )
}
