import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

export function UserProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Restore session from localStorage
    useEffect(() => {
        try {
            const stored = localStorage.getItem('retail-mobile-user');
            if (stored) {
                setUser(JSON.parse(stored));
            }
        } catch (e) {
            console.error('Session restore failed:', e);
        } finally {
            setLoading(false);
        }
    }, []);

    const login = (userData) => {
        setUser(userData);
        localStorage.setItem('retail-mobile-user', JSON.stringify(userData));
    };

    const updateProfile = (updatedData) => {
        const merged = { ...user, ...updatedData };
        setUser(merged);
        localStorage.setItem('retail-mobile-user', JSON.stringify(merged));
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('retail-mobile-user');
    };

    return (
        <UserContext.Provider value={{ user, loading, login, logout, updateProfile }}>
            {children}
        </UserContext.Provider>
    );
}

export const useUser = () => useContext(UserContext);
