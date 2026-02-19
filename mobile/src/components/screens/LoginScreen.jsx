import { useState } from 'react';
import { motion } from 'framer-motion';
import { ShoppingBag, ArrowRight, Mail, User, Eye, EyeOff } from 'lucide-react';

export default function LoginScreen({ onLogin }) {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/customers/mobile-login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: email,
                    name: name || email.split('@')[0],
                    surname: surname || null
                }),
            });

            if (!response.ok) throw new Error('Giriş başarısız');

            const userData = await response.json();
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
            <div className="pt-20 px-8 pb-8">
                <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-200 mb-8">
                    <ShoppingBag size={32} className="text-white" />
                </div>
                <h1 className="text-4xl font-bold text-gray-900 mb-2">Hoş geldin, <br />tekrar.</h1>
                <p className="text-gray-500">Hesabınıza giriş yaparak alışverişe devam edin.</p>
            </div>

            {/* Form */}
            <div className="px-8 flex-1">
                <form onSubmit={handleLogin} className="space-y-4">
                    {/* Name & Surname Row */}
                    <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-1.5">
                            <label className="text-sm font-semibold text-gray-700 ml-1">İsim</label>
                            <div className="relative">
                                <User size={18} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full bg-gray-50 border border-gray-100 rounded-2xl py-3.5 pl-11 pr-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium placeholder:text-gray-400 text-sm"
                                    placeholder="Adınız"
                                    required
                                />
                            </div>
                        </div>
                        <div className="space-y-1.5">
                            <label className="text-sm font-semibold text-gray-700 ml-1">Soyisim</label>
                            <input
                                type="text"
                                value={surname}
                                onChange={(e) => setSurname(e.target.value)}
                                className="w-full bg-gray-50 border border-gray-100 rounded-2xl py-3.5 px-4 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium placeholder:text-gray-400 text-sm"
                                placeholder="Soyadınız"
                            />
                        </div>
                    </div>

                    <div className="space-y-1.5">
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
                        <div className="flex justify-start">
                            <button
                                type="button"
                                onClick={() => {
                                    setName('Ahmet');
                                    setSurname('Yılmaz');
                                    setEmail('demo@stylestore.com');
                                }}
                                className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-1 rounded-lg hover:bg-indigo-100"
                            >
                                Demo Bilgilerini Doldur
                            </button>
                        </div>
                    </div>

                    <motion.button
                        whileTap={{ scale: 0.98 }}
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-indigo-600 text-white rounded-2xl py-4 font-bold text-lg shadow-lg shadow-indigo-200 flex items-center justify-center gap-2 hover:bg-indigo-700 transition-colors disabled:opacity-70 disabled:cursor-not-allowed mt-4"
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


                    <div className="relative my-6">
                        <div className="absolute inset-0 flex items-center">
                            <span className="w-full border-t border-gray-200" />
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                            <span className="bg-white px-2 text-gray-500">Veya şununla devam et</span>
                        </div>
                    </div>

                    <button
                        type="button"
                        onClick={async () => {
                            setIsLoading(true);
                            await new Promise(resolve => setTimeout(resolve, 800));

                            const googleUser = {
                                email: 'merve.yilmaz@gmail.com',
                                name: 'Merve Yılmaz',
                                photo: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop',
                                provider: 'google'
                            };

                            try {
                                const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                                const response = await fetch(`${API_URL}/api/customers/mobile-login`, {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify(googleUser)
                                });

                                if (!response.ok) throw new Error('Google Login Failed');

                                const data = await response.json();
                                onLogin({ ...data, photo_url: data.photo_url || googleUser.photo });
                            } catch (e) {
                                console.error(e);
                                alert("Google ile giriş yapılamadı.");
                            } finally {
                                setIsLoading(false);
                            }
                        }}
                        className="w-full bg-white border border-gray-200 text-gray-700 rounded-2xl py-3.5 font-bold shadow-sm hover:bg-gray-50 hover:border-gray-300 transition-all flex items-center justify-center gap-3"
                    >
                        <svg className="w-5 h-5" viewBox="0 0 24 24">
                            <path
                                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                fill="#4285F4"
                            />
                            <path
                                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                fill="#34A853"
                            />
                            <path
                                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                                fill="#FBBC05"
                            />
                            <path
                                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                fill="#EA4335"
                            />
                        </svg>
                        Google ile Devam Et
                    </button>
                </form>

                <div className="mt-6 text-center">
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
