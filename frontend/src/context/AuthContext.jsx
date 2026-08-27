import { createContext, useContext, useMemo, useState } from "react";
import { apiClient } from "../api/client.js"

const AuthContext = createContext(null);

function decodeToken(token) {
    const payloadSegment = token.split('.')[1];
    return JSON.parse(atob(payloadSegment))
}

export function AuthProvider({children}) {
    //Keeps user logged in even after a page refresh
    const [token, setToken] = useState(() => localStorage.getItem('roboPulseToken'));

    //This only runs when the token changes
    const user = useMemo(() => (token ? decodeToken(token): null), [token]);

    //Authenticates user credentials from frontend
    const login = async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await apiClient.post('/auth/token', formData, {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        });
        localStorage.setItem('roboPulseToken', response.data.access_token);
        setToken(response.data.access_token);
    }

    //Clears authentication session
    const logout = () => {
        localStorage.removeItem('roboPulseToken');
        setToken(null);
    };

    const value = {token, user, isAuthenticated: Boolean(token), login, logout};

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// custom React hook to expose AuthContext to any component
export function useAuth() {
    const context = useContext(AuthContext);

    if (context === null) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context;
}