import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [message, setMessage] = useState('')

  useEffect(() => {
    axios.get('/api/v1/')
      .then(response => {
        setMessage(response.data.message)
      })
      .catch(error => {
        console.error('Error fetching data:', error)
        setMessage('Error connecting to backend')
      })
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-4 text-blue-600">FastAPI + React Boilerplate</h1>
        <p className="text-gray-700">
          Backend says: <span className="font-semibold">{message || 'Loading...'}</span>
        </p>
      </div>
    </div>
  )
}

export default App
