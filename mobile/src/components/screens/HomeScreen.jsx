import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, ArrowRight, Home, Search, Play, Zap, Info, MapPin } from 'lucide-react';
import { HomeSkeleton } from '../common/Skeleton';
import { clsx } from 'clsx';

export default function HomeScreen({ user, onSimulateEnter, onSimulateInStore, onNavigateToShop }) {
    const [isLoading, setIsLoading] = useState(true);
    const [showDevTools, setShowDevTools] = useState(false);

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
        <div className="p-6 pt-12 pb-24 space-y-8 bg-slate-50 min-h-screen">
            {/* Header */}
            <header className="flex justify-between items-start">
                <div onClick={() => setShowDevTools(!showDevTools)}>
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

            {/* AI Insight Card - Premium Glass Effect */}
            <div className="relative overflow-hidden rounded-[2rem] p-6 shadow-2xl transition-transform hover:scale-[1.02] duration-300">
                {/* Dynamic Background */}
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-800"></div>
                <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
                <div className="absolute bottom-0 left-0 w-48 h-48 bg-orange-500/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>

                <div className="relative z-10 text-white">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="bg-white/20 backdrop-blur-md p-1.5 rounded-lg">
                            <Zap size={14} className="text-yellow-300 fill-yellow-300" />
                        </div>
                        <span className="text-xs font-bold tracking-widest opacity-80 uppercase font-heading">AI Asistanı</span>
                    </div>

                    <h3 className="text-2xl font-bold leading-snug mb-3">
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

            {/* Hidden Dev Tools */}
            <AnimatePresence>
                {showDevTools && (
                    <motion.section
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="mt-8 pt-6 border-t border-slate-200 overflow-hidden"
                    >
                        <div className="flex items-center gap-2 mb-4 text-slate-400">
                            <MapPin size={16} />
                            <h2 className="text-xs font-bold uppercase tracking-widest">Geliştirici Paneli</h2>
                        </div>
                        <div className="grid grid-cols-2 gap-3 bg-slate-100 p-4 rounded-2xl">
                            <button onClick={onSimulateEnter} className="p-3 bg-white text-indigo-700 rounded-xl text-xs font-bold shadow-sm hover:shadow-md transition-all text-left">
                                📍 Mağaza Yakını<br />(Geofence)
                            </button>
                            <button onClick={onSimulateInStore} className="p-3 bg-white text-emerald-700 rounded-xl text-xs font-bold shadow-sm hover:shadow-md transition-all text-left">
                                🏪 Mağaza İçi<br />(Beacon)
                            </button>
                        </div>
                        <p className="text-[10px] text-slate-400 mt-2 text-center">
                            Proximity Service: Active • {import.meta.env.VITE_API_URL}
                        </p>
                    </motion.section>
                )}
            </AnimatePresence>
        </div>
    );
}
