import { useState } from 'react';
import { motion } from 'framer-motion';
import { ShoppingBag, ArrowRight, Mail, Lock, Eye, EyeOff } from 'lucide-react';

// import { api } from '../../services/api'; // Legacy API removed

export default function LoginScreen({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);



    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            // Backend API Call
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/customers/mobile-login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    name: email.split('@')[0] // Varsayılan isim
                }),
            });

            if (!response.ok) {
                throw new Error('Giriş başarısız');
            }

            const userData = await response.json();

            // Context'e kaydet
            onLogin(userData);
        } catch (error) {
            console.error("Login Error:", error);
            alert("Giriş yapılırken bir hata oluştu. Lütfen bağlantınızı kontrol edin.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-white relative overflow-hidden flex flex-col">
            {/* Background Decoration */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-50 rounded-full -translate-y-1/2 translate-x-1/2 blur-2xl opacity-60 pointer-events-none" />
            <div className="absolute bottom-0 left-0 w-80 h-80 bg-orange-50 rounded-full translate-y-1/2 -translate-x-1/2 blur-3xl opacity-60 pointer-events-none" />

            {/* Header */}
            <div className="pt-20 px-8 pb-12">
                <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-200 mb-8">
                    <ShoppingBag size={32} className="text-white" />
                </div>
                <h1 className="text-4xl font-bold text-gray-900 mb-2">Hoş geldin, <br />tekrar.</h1>
                <p className="text-gray-500">Hesabınıza giriş yaparak alışverişe devam edin.</p>
            </div>

            {/* Form */}
            <div className="px-8 flex-1">
                <form onSubmit={handleLogin} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-gray-700 ml-1">E-posta</label>
                        <div className="relative">
                            <Mail size={20} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-gray-50 border border-gray-100 rounded-2xl py-4 pl-12 pr-4 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium placeholder:text-gray-400"
                                placeholder="ornek@email.com"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-gray-700 ml-1">Şifre</label>
                        <div className="relative">
                            <Lock size={20} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                            <input
                                type={showPassword ? "text" : "password"}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full bg-gray-50 border border-gray-100 rounded-2xl py-4 pl-12 pr-12 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium placeholder:text-gray-400"
                                placeholder="••••••••"
                                required
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                            >
                                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                            </button>
                        </div>
                        <div className="flex justify-between items-center">
                            <button
                                type="button"
                                onClick={() => {
                                    setEmail('demo@stylestore.com');
                                    setPassword('123456');
                                }}
                                className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-1 rounded-lg hover:bg-indigo-100"
                            >
                                Demo Bilgilerini Doldur
                            </button>
                            <button type="button" className="text-xs font-semibold text-gray-500 hover:text-gray-700">
                                Şifremi unuttum?
                            </button>
                        </div>
                    </div>

                    <motion.button
                        whileTap={{ scale: 0.98 }}
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-indigo-600 text-white rounded-2xl py-4 font-bold text-lg shadow-lg shadow-indigo-200 flex items-center justify-center gap-2 hover:bg-indigo-700 transition-colors disabled:opacity-70 disabled:cursor-not-allowed mt-8"
                    >
                        {isLoading ? (
                            <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                Giriş Yap
                                <ArrowRight size={20} />
                            </>
                        )}
                    </motion.button>
                </form>

                <div className="mt-8 text-center">
                    <p className="text-gray-500 text-sm">
                        Hesabın yok mu?{' '}
                        <button className="text-indigo-600 font-bold hover:underline">
                            Kayıt Ol
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
}
