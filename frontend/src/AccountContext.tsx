import axios from "axios";
import type React from "react";
import { createContext, useContext, useEffect, useState } from "react";


type Account = {
    uuid: string;
    name: string;
    type: string;
    plaid_item_uuid: string
}

type AccountsContextType = {
    accounts: Account[];
    loading: boolean;
    refreshAccounts: () => Promise<void>;
    setAccounts: React.Dispatch<React.SetStateAction<Account[]>>;
}

const AccountsContext = createContext<AccountsContextType | null>(null);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const AccountsProvider = ({ children }: {children: React.ReactNode}) => {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchAccounts = async () => {
        setLoading(true);
        try {
          const res = await axios.get(`${API_BASE_URL}/accounts`, { withCredentials: true });
          setAccounts(res.data.accounts || res.data); 
        } catch (err) {
          setAccounts([]);
        } finally {
          setLoading(false);
        }
    };

    useEffect(() => {
        fetchAccounts();
    }, [])
    return (
        <AccountsContext.Provider value={{
            accounts,
            loading,
            refreshAccounts: fetchAccounts,
            setAccounts,
        }}>
            {children}
        </AccountsContext.Provider>
    );
}

export const useAccounts = () => {
    const context = useContext(AccountsContext);
    if (!context) 
        throw new Error("useUser must be used within a UserProvider");
    return context;
};