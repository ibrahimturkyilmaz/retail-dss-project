import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bell, ArrowRight, Home, Search, Play, Zap } from 'lucide-react';
import { HomeSkeleton } from '../common/Skeleton';

export default function HomeScreen({ user, onSimulateEnter, onSimulateInStore, onNavigateToShop }) {
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Simulate loading delay
        const timer = setTimeout(() => setIsLoading(false), 2000);
        return () => clearTimeout(timer);
    }, []);

    if (!user) return <HomeSkeleton />; // Initial user check
    if (isLoading) return <HomeSkeleton />;

    const categories = [
        { id: 1, name: 'Yeni Gelenler', icon: <Zap size={20} className="text-orange-500" />, color: 'bg-orange-100' },
        { id: 2, name: 'İndirim', icon: <div className="w-5 h-5 border-2 border-cyan-500 rounded-sm" />, color: 'bg-cyan-100' },
        { id: 3, name: 'Kombinler', icon: <div className="w-5 h-5 bg-orange-400 rounded-full" />, color: 'bg-orange-100' },
        { id: 4, name: 'Live', icon: <Play size={20} className="text-indigo-600" />, color: 'bg-indigo-100' },
    ];

    return (
        <div className="p-6 pt-12 pb-24 space-y-6 bg-white min-h-screen">
            {/* Header */}
            <header className="flex justify-between items-start">
                <div>
                    <p className="text-gray-500 text-sm">Hoş geldin,</p>
                    <h1 className="text-2xl font-bold text-gray-900">
                        {user.name} {user.lastname || 'Yılmaz'}
                    </h1>
                </div>
                <div className="relative">
                    <Bell size={24} className="text-gray-700" />
                    <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-white"></span>
                </div>
            </header>

            {/* AI Prediction Card */}
            <div className="bg-white rounded-3xl p-5 shadow-[0_4px_20px_rgba(0,0,0,0.05)] border border-gray-100 relative overflow-hidden">
                <div className="flex items-center gap-2 mb-3">
                    <Zap size={16} className="text-orange-500 fill-orange-500" />
                    <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">AI TAHMİNİ</span>
                </div>

                <div className="flex gap-4 items-center">
                    <div className="w-16 h-16 bg-blue-50 rounded-xl flex items-center justify-center shrink-0">
                        <img src="https://cdn-icons-png.flaticon.com/512/2829/2829824.png" className="w-10 h-10 object-contain opacity-80" alt="Product" />
                    </div>
                    <div className="flex-1">
                        <h3 className="font-bold text-gray-800 leading-tight">Şampuanınız bitmek üzere mi?</h3>
                        <p className="text-xs text-gray-500 mt-1 leading-relaxed">
                            Son siparişinizin üzerinden 45 gün geçti. Tek tıkla yenileyin.
                        </p>
                    </div>
                    <button className="w-10 h-10 bg-gray-900 rounded-full flex items-center justify-center text-white shrink-0">
                        <ArrowRight size={18} />
                    </button>
                </div>
            </div>

            {/* Categories - Swipeable Story Mode */}
            <div className="flex gap-4 overflow-x-auto pb-4 -mx-6 px-6 scrollbar-hide">
                {categories.map((cat) => (
                    <div key={cat.id} className="flex flex-col items-center gap-2 shrink-0">
                        <div className="relative">
                            {/* Gradient Ring */}
                            <motion.div
                                animate={cat.name === 'Live' ? { rotate: 360 } : {}}
                                transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                                className={`w-[72px] h-[72px] rounded-full p-[3px] ${cat.name === 'Live'
                                    ? 'bg-gradient-to-tr from-red-500 via-purple-500 to-orange-500' // Live Ring
                                    : 'bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500' // Standard Ring
                                    }`}
                            >
                                <div className="w-full h-full bg-white rounded-full p-1">
                                    <div className={`w-full h-full rounded-full ${cat.color} flex items-center justify-center relative overflow-hidden`}>
                                        {cat.icon}
                                    </div>
                                </div>
                            </motion.div>

                            {/* "LIVE" Badge */}
                            {cat.name === 'Live' && (
                                <motion.div
                                    animate={{ scale: [1, 1.2, 1] }}
                                    transition={{ duration: 1.5, repeat: Infinity }}
                                    className="absolute -bottom-1 left-1/2 -translate-x-1/2 bg-red-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-full border-2 border-white shadow-sm z-10"
                                >
                                    CANLI
                                </motion.div>
                            )}
                        </div>
                        <span className="text-[11px] font-medium text-gray-700 text-center">{cat.name}</span>
                    </div>
                ))}
            </div>

            {/* Recommended Section */}
            <section>
                <div className="flex justify-between items-end mb-4">
                    <h2 className="text-lg font-bold text-gray-900">Sizin İçin Seçildi</h2>
                    <button
                        onClick={onNavigateToShop}
                        className="text-xs text-indigo-600 font-semibold hover:text-indigo-800 transition-colors"
                    >
                        Tümünü Gör
                    </button>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    {/* Product Card 1 */}
                    <div className="bg-white rounded-2xl border border-gray-100 p-3 shadow-sm relative">
                        <span className="absolute top-3 left-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-lg text-[10px] font-bold shadow-sm z-10">
                            Yüksek İhtimal
                        </span>
                        <div className="aspect-square rounded-xl mb-3 overflow-hidden bg-gray-100 flex items-center justify-center p-2">
                            <img src="./images/leather_jacket.png" className="w-full h-full object-contain mix-blend-multiply" alt="Jacket" />
                        </div>
                        <h4 className="font-bold text-gray-800 text-sm">Vintage Deri Ceket</h4>
                        <p className="text-indigo-600 font-bold text-sm mt-1">4.500 ₺</p>
                    </div>

                    {/* Product Card 2 */}
                    <div className="bg-white rounded-2xl border border-gray-100 p-3 shadow-sm relative">
                        <span className="absolute top-3 left-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-lg text-[10px] font-bold shadow-sm z-10">
                            %20 İndirim
                        </span>
                        <div className="aspect-square rounded-xl mb-3 overflow-hidden bg-gray-100 flex items-center justify-center p-2">
                            <img src="./images/slim_fit_tshirt.png" className="w-full h-full object-contain mix-blend-multiply" alt="Shirt" />
                        </div>
                        <h4 className="font-bold text-gray-800 text-sm">Slim Fit Gömlek</h4>
                        <p className="text-indigo-600 font-bold text-sm mt-1">899 ₺</p>
                    </div>
                </div>
            </section>

            {/* Developer Simulation Tools */}
            <section className="mt-8 border-t border-gray-100 pt-6">
                <h2 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Geliştirici Paneli (Geofence)</h2>
                <div className="grid grid-cols-2 gap-3">
                    <button
                        onClick={onSimulateEnter}
                        className="px-4 py-3 bg-indigo-50 text-indigo-700 rounded-xl text-sm font-semibold hover:bg-indigo-100 transition-colors"
                    >
                        📍 Mağaza Yakını<br />Simüle Et
                    </button>
                    <button
                        onClick={onSimulateInStore}
                        className="px-4 py-3 bg-emerald-50 text-emerald-700 rounded-xl text-sm font-semibold hover:bg-emerald-100 transition-colors"
                    >
                        🏪 Mağaza İçi<br />Simüle Et
                    </button>
                </div>
            </section>
        </div>
    );
}
