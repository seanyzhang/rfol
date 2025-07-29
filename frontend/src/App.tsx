import { useState } from 'react'
import { Routes, Route} from 'react-router-dom'
import Dashboard from './pages/dashboard'
import './App.css'
import Login from './pages/login'
import { UserProvider } from './UserContext'

function App() {
  const [isExiting, setIsExiting] = useState(false)

  return (
    <>
      <UserProvider>
        <main className={"main bg-light flex flex-col no-scrollbar"}>
          <Routes>
            <Route path="/" element={<Dashboard isExiting={isExiting}/>} />
            <Route path="/login" element={<Login isExiting={isExiting}/>} />
          </Routes>
        </main>
      </UserProvider>
    </>
  )
}

export default App
