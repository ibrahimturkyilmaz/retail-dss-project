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
                setLoading(false);
                return;
            }
        } else if (type === 'FIELD') {
            if (!isMobile) {
                // For testing purposes, we might allow it, but user requested restriction.
                // Strict check: if (isDesktop) ...
                setError('⚠️ Saha operasyonuna sadece mobil cihazlardan erişilebilir.');
                setLoading(false);
                return;
            }
        }

        try {
            await login(email, password);
            // Başarılı ise App.jsx içindeki routing zaten yönlendirecek
        } catch (err) {
            setError('Giriş başarısız. Bilgilerinizi kontrol edin.');
        } finally {
            setLoading(false);
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await signUp(email, password, {
                role: 'user',
                department: 'Genel',
                first_name: 'Yeni',
                last_name: 'Kullanıcı'
            });
            alert('Kayıt başarılı! Lütfen e-postanızı doğrulayın.');
            setIsLogin(true); // Giriş ekranına dön
        } catch (err) {
            if (err.message?.includes('already registered')) {
                setError('Bu e-posta adresi zaten kayıtlı. Lütfen giriş yapmayı deneyin.');
            } else {
                setError(err.message || 'Kayıt olurken bir hata oluştu.');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = async () => {
        try {
            setLoading(true);
            await signInWithGoogle();
        } catch (error) {
            setError('Google ile giriş yapılırken hata oluştu.');
        } finally {
            setLoading(false);
        }
    };

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
                        <>
                            <button
                                type="button"
                                onClick={handleGoogleLogin}
                                disabled={loading}
                                className="w-full bg-white text-slate-700 border border-slate-300 py-3 rounded-xl font-bold hover:bg-slate-50 transition-all flex items-center justify-center gap-2 mb-3"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" className="w-5 h-5">
                                    <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z" />
                                    <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z" />
                                    <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z" />
                                    <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z" />
                                </svg>
                                Google ile {isLogin ? 'Giriş Yap' : 'Kayıt Ol'}
                            </button>

                            <button
                                type="submit"
                                className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg transform transition-all hover:scale-[1.02] active:scale-[0.98]"
                            >
                                Kayıt Ol ve Başla
                            </button>
                        </>
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
