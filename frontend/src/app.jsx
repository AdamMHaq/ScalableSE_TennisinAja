import React, { useState } from 'react'

const API_URL = 'http://localhost:8000/users'

function App() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [token, setToken] = useState('')
  const [mode, setMode] = useState('login') // 'login' or 'register'

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const endpoint = mode === 'register' ? '/register' : '/login'

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      const data = await response.json()
      if (response.ok) {
        setToken(data.access_token || 'Registered successfully!')
      } else {
        alert(data.detail || 'Failed')
      }
    } catch (error) {
      console.error('Error:', error)
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto', textAlign: 'center' }}>
      <h1>TennisinAja - {mode === 'login' ? 'Login' : 'Register'}</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
          style={{ margin: '0.5rem', width: '100%' }}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
          style={{ margin: '0.5rem', width: '100%' }}
        />
        <button type="submit" style={{ marginTop: '1rem' }}>
          {mode === 'login' ? 'Login' : 'Register'}
        </button>
      </form>
      <p style={{ marginTop: '1rem' }}>
        {mode === 'login' ? (
          <>
            No account?{' '}
            <button onClick={() => setMode('register')}>Register</button>
          </>
        ) : (
          <>
            Already have an account?{' '}
            <button onClick={() => setMode('login')}>Login</button>
          </>
        )}
      </p>
      {token && (
        <div style={{ marginTop: '1rem', wordBreak: 'break-word' }}>
          <strong>Response:</strong>
          <pre>{token}</pre>
        </div>
      )}
    </div>
  )
}

export default App
