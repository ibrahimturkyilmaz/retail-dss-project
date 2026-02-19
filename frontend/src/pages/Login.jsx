import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { UserCircleIcon, LockClosedIcon, BuildingOfficeIcon, DevicePhoneMobileIcon } from '@heroicons/react/24/outline';
import { isMobile, isDesktop } from 'react-device-detect';

const Login = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login, signUp } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const from = location.state?.from?.pathname || '/';

    const handleLogin = async (type) => {
        setError('');

        // Device Validation
        if (type === 'OFFICE') {
            if (isMobile) {
                setError('⚠️ Ofis paneline sadece bilgisayardan veya tabletten erişilebilir.');
                return;
            }
        } else if (type === 'FIELD') {
            if (!isMobile) {
                // For testing purposes, we might allow it, but user requested restriction.
                // Strict check: if (isDesktop) ...
                // Let's stick to the rule: "Saha ise !isMobile -> Hata"
                setError('⚠️ Saha operasyonuna sadece mobil cihazlardan erişilebilir.');
                return;
            }
        }

        try {
            await login(email, password);

            if (type === 'FIELD') {
                navigate('/pos');
            } else {
                navigate(from, { replace: true });
            }

        } catch (err) {
            console.error(err);
            setError(err.message || 'Giriş başarısız.');
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await signUp(email, password);
            setError('Kayıt başarılı! Giriş yapabilirsiniz.');
            setIsLogin(true);
        } catch (err) {
            setError(err.message || 'Kayıt başarısız.');
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-slate-900 overflow-hidden relative">
            {/* Background Ambience */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
                <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-600/20 rounded-full blur-[120px] animate-blob" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-purple-600/20 rounded-full blur-[120px] animate-blob animation-delay-2000" />
            </div>

            <div className="relative z-10 w-full max-w-md p-8 bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl">
                <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-white mb-2">{isLogin ? 'Hoş Geldiniz' : 'Hesap Oluştur'}</h2>
                    <p className="text-slate-300">{isLogin ? 'Operasyon Tipini Seçerek Giriş Yapın' : 'Yeni bir RetailDSS hesabı başlatın'}</p>
                </div>

                {error && (
                    <div className={`mb-4 p-3 rounded-lg text-sm text-center ${error.includes('başarılı') ? 'bg-green-500/20 border border-green-500/50 text-green-200' : 'bg-red-500/20 border border-red-500/50 text-red-200'}`}>
                        {error}
                    </div>
                )}

                <form onSubmit={isLogin ? (e) => e.preventDefault() : handleSignup} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">E-posta Adresi</label>
                        <div className="relative">
                            <UserCircleIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                placeholder="ornek@sirket.com"
                                required
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">Şifre</label>
                        <div className="relative">
                            <LockClosedIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                placeholder="••••••••"
                                required
                                minLength={6}
                            />
                        </div>
                    </div>

                    {isLogin && (
                        <div className="pt-2">
                            <label className="block text-sm font-medium text-slate-400 mb-2">Hızlı Giriş (Demo Hesaplar)</label>
                            <select
                                onChange={(e) => {
                                    if (e.target.value) {
                                        setEmail(e.target.value);
                                        setPassword("123456");
                                    }
                                }}
                                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
                            >
                                <option value="">Hesap Seçin...</option>
                                <option value="admin@retaildss.com">Admin (Yönetici)</option>
                                <option value="user1@retaildss.com">Mağaza Müdürü 1</option>
                            </select>
                        </div>
                    )}

                    {isLogin ? (
                        <div className="flex gap-4 pt-2">
                            <button
                                type="button"
                                onClick={() => handleLogin('OFFICE')}
                                className="flex-1 flex flex-col items-center justify-center py-4 px-2 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-xl transition-all border border-slate-600 hover:border-blue-500 group"
                            >
                                <BuildingOfficeIcon className="w-8 h-8 mb-2 text-blue-400 group-hover:scale-110 transition-transform" />
                                Ofis Girişi
                            </button>
                            <button
                                type="button"
                                onClick={() => handleLogin('FIELD')}
                                className="flex-1 flex flex-col items-center justify-center py-4 px-2 bg-gradient-to-br from-indigo-900 to-purple-900 hover:from-indigo-800 hover:to-purple-800 text-white font-semibold rounded-xl transition-all border border-purple-500/30 hover:border-purple-400 shadow-lg group"
                            >
                                <DevicePhoneMobileIcon className="w-8 h-8 mb-2 text-purple-300 group-hover:scale-110 transition-transform" />
                                Saha Girişi
                            </button>
                        </div>
                    ) : (
                        <button
                            type="submit"
                            className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg transform transition-all hover:scale-[1.02] active:scale-[0.98]"
                        >
                            Kayıt Ol ve Başla
                        </button>
                    )}
                </form>

                <div className="mt-6 text-center text-sm text-slate-400">
                    {isLogin ? (
                        <p>Hesabınız yok mu? <button onClick={() => { setIsLogin(false); setError(''); }} className="text-blue-400 hover:text-blue-300 font-semibold ml-1">Kayıt Olun</button></p>
                    ) : (
                        <p>Zaten hesabınız var mı? <button onClick={() => { setIsLogin(true); setError(''); }} className="text-blue-400 hover:text-blue-300 font-semibold ml-1">Giriş Yapın</button></p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Login;
