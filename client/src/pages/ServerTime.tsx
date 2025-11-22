import { useEffect, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || ''

function ServerTime() {
  const [serverTime, setServerTime] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const apiEndpoint = import.meta.env.DEV ? '/api/servertime' : `${API_URL}/api/servertime`
    fetch(apiEndpoint)
      .then(res => res.json())
      .then(data => {
        setServerTime(data.time)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-4">Server Time</h1>
      {loading && <p className="text-slate-600">Loading...</p>}
      {error && <p className="text-red-600">Error: {error}</p>}
      {serverTime && (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <p className="text-slate-600 text-sm mb-2">Current server time (UTC):</p>
          <p className="text-2xl font-mono text-slate-900">{new Date(serverTime).toLocaleString()}</p>
          <p className="text-slate-500 text-sm mt-2">ISO: {serverTime}</p>
        </div>
      )}
    </div>
  )
}

export default ServerTime
