import { useState } from 'react'
import { Routes, Route, useNavigate} from 'react-router-dom'
import { ANIMATION_DELAYS } from './constants'
import { logger } from './utils/logger'
import Dashboard from './pages/dashboard'
import './App.css'
import SideBar from './components/SideBar'
import Login from './pages/login'

function App() {
  const [isExiting, setIsExiting] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const navigate = useNavigate(); 

  const navTo = (address: string) => {
    logger.log("Navigating to", address === "/" ? "dashboard" : (address ?? "dashboard"));
    setIsExiting(true);
    setTimeout (() => {
      navigate(`/${address}`);
      setTimeout(() => {
        setIsExiting(false);
      }, 50);
    }, ANIMATION_DELAYS.TRANSITION)
  }

  return (
    <>
      <main className={"bg-light container overflow-hidden no-scrollbar h-[100vh]"}>
        {isLoggedIn ?? <SideBar/>}
        <Routes>
          <Route path="/" element={<Dashboard isExiting={isExiting}/>} />
          <Route path="/login" element={<Login isExiting={isExiting}/>} />
        </Routes>
      </main>
    </>
  )
}

export default App
