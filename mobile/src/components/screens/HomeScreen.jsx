import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, ArrowRight, Search, Play, Zap, Info, MapPin, Navigation } from 'lucide-react';
import { HomeSkeleton } from '../common/Skeleton';
import { clsx } from 'clsx';
import { useLocation } from '../../context/LocationContext';

export default function HomeScreen({ user, onSimulateEnter, onSimulateInStore, onNavigateToShop, onNavigateToProfile }) {
    const [isLoading, setIsLoading] = useState(true);
    const { locationEnabled, address } = useLocation();

    useEffect(() => {
        const timer = setTimeout(() => setIsLoading(false), 2000);
        return () => clearTimeout(timer);
    }, []);

    if (!user) return <HomeSkeleton />;
    if (isLoading) return <HomeSkeleton />;

    const categories = [
        { id: 1, name: 'Yeni Sezon', icon: <Zap size={20} className="text-white" />, color: 'bg-gradient-to-br from-orange-400 to-red-500' },
        { id: 2, name: 'İndirim', icon: <span className="text-white font-bold text-lg">%</span>, color: 'bg-gradient-to-br from-blue-400 to-indigo-600' },
        { id: 3, name: 'Kombinler', icon: <Search size={20} className="text-white" />, color: 'bg-gradient-to-br from-emerald-400 to-teal-600' },
        { id: 4, name: 'Live', icon: <Play size={20} className="text-white fill-white" />, color: 'bg-gradient-to-br from-purple-500 to-pink-600' },
    ];

    return (
        <div className="p-6 pt-12 pb-32 space-y-8 bg-slate-50 min-h-screen">
            {/* Header */}
            <header className="flex justify-between items-start">
                <div>
                    <p className="text-slate-500 text-sm font-medium mb-1">Tekrar hoş geldin,</p>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                        {user.name}
                    </h1>
                </div>
                <div className="relative p-2 bg-white rounded-full shadow-sm border border-slate-100">
                    <Bell size={24} className="text-slate-700" />
                    <span className="absolute top-2 right-2 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white"></span>
                </div>
            </header>

            {/* Location Permission Request Card */}
            {!locationEnabled && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-700 rounded-[1.5rem] p-5 shadow-xl shadow-indigo-200/50 text-white cursor-pointer active:scale-[0.98] transition-transform"
                    onClick={onNavigateToProfile}
                >
                    <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-sm shrink-0 border border-white/10">
                            <Navigation size={22} className="text-white" />
                        </div>
                        <div className="flex-1">
                            <h3 className="font-bold text-base mb-1">📍 Konumunuzu Açın</h3>
                            <p className="text-xs text-indigo-100 leading-relaxed opacity-90">
                                Yakınındaki mağazaları gör, özel kampanyalardan haberdar ol ve mağaza içi tekliflerden yararlan!
                            </p>
                        </div>
                    </div>
                    <div className="flex gap-2 mt-4">
                        <div className="bg-white/15 backdrop-blur-sm rounded-xl px-3 py-1.5 text-[10px] font-bold border border-white/10">🏪 Yakın Mağaza</div>
                        <div className="bg-white/15 backdrop-blur-sm rounded-xl px-3 py-1.5 text-[10px] font-bold border border-white/10">🎯 Özel Kampanya</div>
                        <div className="bg-white/15 backdrop-blur-sm rounded-xl px-3 py-1.5 text-[10px] font-bold border border-white/10">🔔 Bildirim</div>
                    </div>
                </motion.div>
            )}

            {/* Live Location Display (If Enabled) */}
            {locationEnabled && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100 flex items-center gap-3"
                >
                    <div className="relative">
                        <div className="w-10 h-10 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600">
                            <MapPin size={18} />
                        </div>
                        <span className="absolute -top-0.5 -right-0.5 w-3 h-3 bg-emerald-500 rounded-full border-2 border-white animate-pulse" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-slate-400 text-[10px] font-bold uppercase tracking-wide">Canlı Konum</p>
                        <p className="text-slate-700 font-bold text-sm truncate">
                            {address ? address.short : 'Konum alınıyor...'}
                        </p>
                    </div>
                    <div className="text-right shrink-0">
                        <p className="text-[10px] text-slate-400 font-semibold">En Yakın Mağaza</p>
                        <p className="text-xs text-indigo-600 font-bold">0.8 km</p>
                    </div>
                </motion.div>
            )}

            {/* AI Insight Card - Premium Glass Effect */}
            <div className="relative overflow-hidden rounded-[2rem] p-6 shadow-xl transition-transform hover:scale-[1.02] duration-300 group">
                {/* Dynamic Background */}
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-800 transition-all group-hover:bg-indigo-700"></div>
                <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
                <div className="absolute bottom-0 left-0 w-48 h-48 bg-orange-500/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>

                <div className="relative z-10 text-white">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="bg-white/20 backdrop-blur-md p-1.5 rounded-lg border border-white/10">
                            <Zap size={14} className="text-yellow-300 fill-yellow-300" />
                        </div>
                        <span className="text-xs font-bold tracking-widest opacity-80 uppercase font-heading">AI Asistanı</span>
                    </div>

                    <h3 className="text-2xl font-bold leading-snug mb-3 font-heading">
                        Şampuan rezervin <br />
                        <span className="text-indigo-200">bitmek üzere!</span>
                    </h3>

                    <p className="text-indigo-100 text-sm mb-6 leading-relaxed opacity-90 max-w-[85%]">
                        Son alışverişinizden bu yana 45 gün geçti. Rutininiz bozulmasın diye sizin için hazırladık.
                    </p>

                    <div className="flex gap-3">
                        <button className="flex-1 bg-white text-indigo-900 py-3.5 px-6 rounded-xl font-bold text-sm hover:bg-indigo-50 transition-colors shadow-lg shadow-black/10">
                            Sepete Ekle
                        </button>
                        <button className="w-12 h-12 bg-white/10 backdrop-blur-md rounded-xl flex items-center justify-center hover:bg-white/20 transition-colors border border-white/10">
                            <Info size={20} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Stories Section */}
            <div>
                <div className="flex justify-between items-end mb-4 px-1">
                    <h2 className="text-lg font-bold text-slate-900">Koleksiyonlar</h2>
                    <span className="text-xs text-indigo-600 font-semibold cursor-pointer">Tümü</span>
                </div>
                <div className="flex gap-5 overflow-x-auto pb-6 -mx-6 px-6 hide-scrollbar">
                    {categories.map((cat) => (
                        <div key={cat.id} className="flex flex-col items-center gap-3 shrink-0 group cursor-pointer">
                            <div className="relative">
                                {/* Gradient Ring */}
                                <div className={clsx(
                                    "w-[76px] h-[76px] rounded-full p-[3px] transition-transform duration-300 group-hover:scale-105",
                                    cat.name === 'Live'
                                        ? "bg-gradient-to-tr from-red-500 via-orange-500 to-yellow-500 animate-spin-slow"
                                        : "bg-gradient-to-tr from-slate-200 to-slate-300 group-hover:from-indigo-400 group-hover:to-purple-400"
                                )}>
                                    <div className="w-full h-full bg-white rounded-full p-1">
                                        <div className={`w-full h-full rounded-full ${cat.color} flex items-center justify-center shadow-inner`}>
                                            {cat.icon}
                                        </div>
                                    </div>
                                </div>
                                {cat.name === 'Live' && (
                                    <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 bg-red-600 text-white text-[10px] font-bold px-2.5 py-0.5 rounded-full border-2 border-white shadow-sm">
                                        CANLI
                                    </div>
                                )}
                            </div>
                            <span className="text-xs font-semibold text-slate-700 group-hover:text-indigo-600 transition-colors">
                                {cat.name}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Recommended Products */}
            <section>
                <div className="flex justify-between items-end mb-5 px-1">
                    <h2 className="text-xl font-bold text-slate-900">Sizin İçin Seçildi</h2>
                    <button onClick={onNavigateToShop} className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-slate-200 transition-colors">
                        <ArrowRight size={16} />
                    </button>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    {/* Card 1 */}
                    <div className="card group cursor-pointer">
                        <div className="p-3 pb-0">
                            <div className="relative aspect-[4/5] bg-slate-50 rounded-2xl overflow-hidden mb-3">
                                <span className="absolute top-3 left-3 bg-white/90 backdrop-blur text-indigo-900 text-[10px] font-bold px-2 py-1 rounded-md shadow-sm z-10 uppercase tracking-wide">
                                    %98 Eşleşme
                                </span>
                                <img src="./images/leather_jacket.png" className="w-full h-full object-contain mix-blend-multiply group-hover:scale-110 transition-transform duration-500" alt="Jacket" />
                            </div>
                        </div>
                        <div className="px-4 pb-4">
                            <h4 className="font-bold text-slate-900 text-sm mb-1 leading-snug">Vintage Deri Ceket</h4>
                            <div className="flex justify-between items-center">
                                <span className="text-indigo-600 font-bold">4.500 ₺</span>
                                <button className="w-7 h-7 rounded-full bg-slate-900 text-white flex items-center justify-center hover:bg-indigo-600 transition-colors">
                                    <ArrowRight size={14} />
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Card 2 */}
                    <div className="card group cursor-pointer">
                        <div className="p-3 pb-0">
                            <div className="relative aspect-[4/5] bg-slate-50 rounded-2xl overflow-hidden mb-3">
                                <span className="absolute top-3 left-3 bg-red-500 text-white text-[10px] font-bold px-2 py-1 rounded-md shadow-sm z-10 uppercase tracking-wide">
                                    İndirim
                                </span>
                                <img src="./images/slim_fit_tshirt.png" className="w-full h-full object-contain mix-blend-multiply group-hover:scale-110 transition-transform duration-500" alt="Shirt" />
                            </div>
                        </div>
                        <div className="px-4 pb-4">
                            <h4 className="font-bold text-slate-900 text-sm mb-1 leading-snug">Slim Fit Gömlek</h4>
                            <div className="flex justify-between items-center">
                                <span className="text-indigo-600 font-bold">899 ₺</span>
                                <button className="w-7 h-7 rounded-full bg-slate-900 text-white flex items-center justify-center hover:bg-indigo-600 transition-colors">
                                    <ArrowRight size={14} />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Developer / Simulation Tools - VISIBLE */}
            <section className="mt-8 pt-6 border-t border-slate-200">
                <div className="flex items-center gap-2 mb-4 text-slate-500">
                    <MapPin size={16} />
                    <h2 className="text-xs font-bold uppercase tracking-widest">Geliştirici / Simülasyon</h2>
                </div>
                <div className="grid grid-cols-2 gap-3 bg-slate-100 p-4 rounded-2xl border border-slate-200">
                    <button onClick={onSimulateEnter} className="p-3 bg-white text-indigo-700 rounded-xl text-xs font-bold shadow-sm hover:shadow-md transition-all text-left flex items-center gap-2 group">
                        <div className="w-8 h-8 rounded-full bg-indigo-50 flex items-center justify-center group-hover:bg-indigo-100 transition-colors">
                            <MapPin size={16} />
                        </div>
                        <span>Mağaza Yakını<br />(Geofence)</span>
                    </button>
                    <button onClick={onSimulateInStore} className="p-3 bg-white text-emerald-700 rounded-xl text-xs font-bold shadow-sm hover:shadow-md transition-all text-left flex items-center gap-2 group">
                        <div className="w-8 h-8 rounded-full bg-emerald-50 flex items-center justify-center group-hover:bg-emerald-100 transition-colors">
                            <Zap size={16} />
                        </div>
                        <span>Mağaza İçi<br />(Beacon)</span>
                    </button>
                </div>
                <p className="text-[10px] text-slate-400 mt-2 text-center font-mono">
                    Proximity Service • {import.meta.env.VITE_API_URL}
                </p>
            </section>
        </div>
    );
}
