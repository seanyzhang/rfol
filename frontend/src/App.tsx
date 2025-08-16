import { useState } from 'react'
import { Routes, Route} from 'react-router-dom'
import Dashboard from './pages/dashboard'
import './App.css'
import Login from './pages/login'
import { UserProvider } from './UserContext'
import { AccountsProvider } from './AccountContext'

function App() {
    const [isExiting, setIsExiting] = useState(false)

    return (
        <>
            <UserProvider>
                <AccountsProvider>
                    <main className={"main bg-light flex flex-col no-scrollbar"}>
                        <Routes>
                            <Route path="/" element={<Dashboard isExiting={isExiting}/>} />
                            <Route path="/login" element={<Login isExiting={isExiting}/>} />
                        </Routes>
                    </main>
                </AccountsProvider>
            </UserProvider>
        </>
    )
}

export default App
