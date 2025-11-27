import { useEffect, useState } from 'react'

export default function ServerTime() {
  const [serverTime, setServerTime] = useState<string>('')

  useEffect(() => {
    fetch('/api/servertime')
      .then(res => res.json())
      .then(data => setServerTime(data.time))
  }, [])

  if (!serverTime) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">Server Time!</h1>
        <p className="text-slate-600">Loading...</p>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-4">Server Time!</h1>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
        <p className="text-slate-600 text-sm mb-2">Current server time (UTC):</p>
        <p className="text-2xl font-mono text-slate-900">{new Date(serverTime).toLocaleString()}</p>
        <p className="text-slate-500 text-sm mt-2">ISO: {serverTime}</p>
      </div>
    </div>
  )
}
