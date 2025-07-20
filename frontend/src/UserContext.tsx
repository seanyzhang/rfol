import axios from "axios";
import { createContext, useContext, useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type User = {
    uuid: string;
    username: string;
    first_name: string;
    last_name: string;
  };
  
type UserContextType = {
    currentUser: User | null;
    setCurrentUser: (user: User | null) => void;
    loading: boolean;
    logout: () => Promise<void>;
};
  
const UserContext = createContext<UserContextType | null>(null);
  
export const UserProvider = ({ children }: { children: React.ReactNode }) => {
    const [currentUser, setCurrentUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
  
    const getCurrentSession = async () => {
        try {
            const res = await axios.get(`${API_BASE_URL}/session`, {withCredentials: true});
            setCurrentUser(res.data)
        } catch (err) {
            setCurrentUser(null);
        } finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        try {
            const sessionId = document.cookie.split("; ").find((row) => row.startsWith("session_id="))?.split("=")[1];
    
            await axios.post(
            `${API_BASE_URL}/session/logout`,
            { session_id: sessionId },
            { withCredentials: true }
            );
            setCurrentUser(null);
        } catch (err) {
            console.error("Logout failed:", err);
        }
    };
  
    useEffect(() => {
        getCurrentSession();
    }, []);
  
    return (
        <UserContext.Provider value={{ currentUser, setCurrentUser, loading, logout }}>
            {children}
        </UserContext.Provider>
    );
};
  
export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) 
        throw new Error("useUser must be used within a UserProvider");
    return context;
};
