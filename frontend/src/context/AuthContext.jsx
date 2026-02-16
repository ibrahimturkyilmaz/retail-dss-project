import React, { createContext, useContext, useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [session, setSession] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Mevcut oturumu kontrol et
        supabase.auth.getSession().then(({ data: { session } }) => {
            setSession(session);

            const sbUser = session?.user;
            if (sbUser) {
                sbUser.username = sbUser.user_metadata?.username || sbUser.email?.split('@')[0];
            }

            setUser(sbUser ?? null);
            setLoading(false);
        });

        // Oturum değişikliklerini dinle
        const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
            setSession(session);

            // Supabase user objesini zenginleştir
            const sbUser = session?.user;
            if (sbUser) {
                // Username yoksa email'den türet (Geriye dönük uyumluluk)
                sbUser.username = sbUser.user_metadata?.username || sbUser.email?.split('@')[0];
            }

            setUser(sbUser ?? null);
            setLoading(false);
        });

        return () => subscription.unsubscribe();
    }, []);

    const login = async (email, password) => {
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });

        if (error) throw error;
        return data;
    };

    const signUp = async (email, password, metadata = {}) => {
        const { data, error } = await supabase.auth.signUp({
            email,
            password,
            options: {
                data: metadata, // Ad, Soyad, Rol vb.
            },
        });

        if (error) throw error;
        return data;
    };

    const logout = async () => {
        const { error } = await supabase.auth.signOut();
        if (error) throw error;
        setUser(null);
        setSession(null);
    };

    return (
        <AuthContext.Provider value={{ user, session, loading, login, signUp, logout }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
