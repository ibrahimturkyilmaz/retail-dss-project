import React, { createContext, useContext, useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';

const UserContext = createContext();

export function UserProvider({ children }) {
    const [user, setUser] = useState(null);
    const [session, setSession] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Mevcut oturumu kontrol et
        const initSession = async () => {
            const { data: { session } } = await supabase.auth.getSession();
            setSession(session);
            if (session?.user?.email) {
                await fetchBackendCustomer(session.user);
            } else {
                setLoading(false);
            }
        };
        initSession();

        // Oturum değişikliklerini dinle
        const { data: { subscription } } = supabase.auth.onAuthStateChange(async (_event, session) => {
            console.log("Auth State Changed:", _event, session);
            setSession(session);
            if (session?.user?.email) {
                await fetchBackendCustomer(session.user);
            } else {
                setUser(null);
                setLoading(false);
            }
        });

        return () => subscription.unsubscribe();
    }, []);

    const fetchBackendCustomer = async (supabaseUser) => {
        try {
            const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const res = await fetch(`${API_URL}/api/customers/mobile-login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: supabaseUser.email,
                    name: supabaseUser.user_metadata?.full_name || supabaseUser.email.split('@')[0],
                    photo: supabaseUser.user_metadata?.avatar_url
                })
            });

            if (res.ok) {
                const customer = await res.json();
                setUser(customer); // Backend customer with Integer ID
            } else {
                console.error("Failed to sync user with backend");
            }
        } catch (error) {
            console.error("Error fetching customer:", error);
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });
        if (error) throw error;
        return data;
    };

    const signInWithGoogle = async () => {
        try {
            const { data, error } = await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: window.location.origin
                }
            });
            if (error) throw error;
            return data;
        } catch (error) {
            throw error;
        }
    };

    const logout = async () => {
        const { error } = await supabase.auth.signOut();
        if (error) throw error;
        setUser(null);
        setSession(null);
    };

    const updateProfile = (updatedData) => {
        // Supabase metadata update logic could go here
        // For now, just local state update as placeholder if needed
        const merged = { ...user, ...updatedData };
        setUser(merged);
    };

    return (
        <UserContext.Provider value={{
            user,
            session,
            loading,
            login,
            logout,
            signInWithGoogle,
            updateProfile
        }}>
            {!loading && children}
        </UserContext.Provider>
    );
}

export const useUser = () => useContext(UserContext);
