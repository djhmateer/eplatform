import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

interface User {
  id: number
  email: string
}

export default function Users() {
  const [users, setUsers] = useState<User[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/users', { credentials: 'include' })
      .then(res => {
        if (!res.ok) {
          throw new Error(res.status === 401 ? 'You must be logged in to view users' : 'Failed to load users')
        }
        return res.json()
      })
      .then(data => setUsers(data.users))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">Users</h1>
        <p className="text-slate-600">Loading...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-4">Users</h1>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">{error}</p>
          <Link to="/login" className="mt-2 inline-block text-red-700 underline hover:text-red-800">
            Go to Login
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-4">Users</h1>
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Email</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {users.map(user => (
              <tr key={user.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 text-sm text-slate-900">{user.id}</td>
                <td className="px-6 py-4 text-sm text-slate-600">{user.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
