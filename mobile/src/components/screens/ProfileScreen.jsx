import React, { useState } from 'react';
import { Award, Zap, Settings, Star, Gift, ChevronRight, MoreHorizontal, User, ToggleLeft, ToggleRight, X, AlertTriangle, ShoppingBag, Heart, MapPin, CreditCard, HelpCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useUser } from '../../context/UserContext';
import { useLocation } from '../../context/LocationContext';

export default function ProfileScreen({ notificationsEnabled, setNotificationsEnabled }) {
    const { user } = useUser();
    const {
        location: userLocation,
        address: userAddress,
        locationEnabled,
        setLocationEnabled,
        requestPermission: requestLocationPermission,
        isLoading
    } = useLocation();

    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [showLocationWarning, setShowLocationWarning] = useState(false);

    if (!user) return null;

    const handleLocationToggle = () => {
        if (locationEnabled) {
            // Trying to turn off -> show warning
            setShowLocationWarning(true);
            setIsSettingsOpen(false); // Close settings to show warning focused
        } else {
            requestLocationPermission();
        }
    };

    const confirmDisableLocation = () => {
        setLocationEnabled(false);
        setShowLocationWarning(false);
    };

    return (
        <div className="bg-gray-50 min-h-screen pb-24">
            {/* Dark Header Section */}
            <div className="bg-[#1a1f36] text-white pt-12 pb-10 rounded-b-[40px] px-6 relative overflow-hidden">
                {/* Background Glows */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-64 bg-yellow-500/10 rounded-full blur-[80px]"></div>

                <header className="flex justify-end items-center mb-8 relative z-10 w-full">
                    {/* Settings Button (Three Dots) - Moved to right since time is gone */}
                    <button
                        onClick={() => setIsSettingsOpen(true)}
                        className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center backdrop-blur-md hover:bg-white/20 transition-colors z-50 pointer-events-auto cursor-pointer"
                    >
                        <MoreHorizontal size={20} className="text-white" />
                    </button>
                </header>

                <div className="flex flex-col items-center relative z-10">
                    {/* Animated Star Container */}
                    <div className="relative mb-4">
                        {/* Main Pulsing Ring */}
                        <motion.div
                            animate={{ scale: [1, 1.1, 1], opacity: [0.5, 0.2, 0.5] }}
                            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                            className="absolute inset-0 bg-yellow-400/30 rounded-full blur-xl"
                        />

                        {/* Random Twinkling Stars */}
                        {[...Array(6)].map((_, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, scale: 0 }}
                                animate={{
                                    opacity: [0, 1, 0],
                                    scale: [0.5, 1, 0.5],
                                    x: Math.random() * 80 - 40,
                                    y: Math.random() * 80 - 40
                                }}
                                transition={{
                                    duration: 2,
                                    repeat: Infinity,
                                    delay: i * 0.4,
                                    repeatDelay: Math.random()
                                }}
                                className="absolute left-1/2 top-1/2 w-2 h-2 text-yellow-300"
                            >
                                <Star size={12} fill="currentColor" />
                            </motion.div>
                        ))}

                        {/* Main Gold Circle */}
                        <motion.div
                            animate={{ scale: [1, 1.05, 1] }}
                            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                            className="w-32 h-32 rounded-full bg-[#1a1f36] border-4 border-yellow-500 flex items-center justify-center shadow-[0_0_30px_rgba(234,179,8,0.3)] relative z-20"
                        >
                            <div className="w-24 h-24 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center shadow-inner">
                                <Star size={48} className="text-white fill-white" />
                            </div>
                        </motion.div>
                    </div>

                    <h1 className="text-2xl font-bold text-yellow-400 mb-1">Gold Üye</h1>
                    <p className="text-gray-400 text-sm mb-2">{user.name} {user.lastname || 'Yılmaz'}</p>

                    {/* Location Badge */}
                    <LocationBadge locationEnabled={locationEnabled} userLocation={userLocation} userAddress={userAddress} />

                    {/* Progress Bar */}
                    <div className="w-full max-w-xs">
                        <div className="flex justify-between text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">
                            <span>Mevcut Puan: 1.250</span>
                            <span>Platinum: 2.000</span>
                        </div>
                        <div className="h-3 bg-gray-700 rounded-full overflow-hidden relative">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: "62%" }}
                                transition={{ duration: 1.5, ease: "easeOut" }}
                                className="h-full bg-gradient-to-r from-yellow-500 to-yellow-300 rounded-full"
                            />
                        </div>
                        <p className="text-[10px] text-gray-400 mt-2 text-center font-medium opacity-80">
                            🚀 Bir sonraki seviye için <span className="text-yellow-400 font-bold">2 sipariş</span> daha ver!
                        </p>
                    </div>
                </div>
            </div>

            {/* Content Sections */}
            <div className="px-6 -mt-6 relative z-30 space-y-4">
                {/* Active Coupons */}
                <div className="bg-white rounded-2xl p-4 shadow-sm flex items-center gap-4 cursor-pointer hover:bg-gray-50 transition-colors">
                    <div className="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center text-purple-600">
                        <Gift size={24} />
                    </div>
                    <div className="flex-1">
                        <h3 className="font-bold text-gray-900">Aktif Kuponlarım</h3>
                        <p className="text-xs text-gray-500">3 adet kullanılabilir indirim</p>
                    </div>
                    <ChevronRight size={20} className="text-gray-300" />
                </div>

                {/* New Menu Items */}
                <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
                    {[
                        { icon: ShoppingBag, label: 'Siparişlerim', sub: 'Son sipariş: 2 gün önce', color: 'text-blue-600', bg: 'bg-blue-50' },
                        { icon: Heart, label: 'Favorilerim', sub: '12 kayıtlı ürün', color: 'text-red-500', bg: 'bg-red-50' },
                        { icon: MapPin, label: 'Adreslerim', sub: 'Ev, İş', color: 'text-orange-500', bg: 'bg-orange-50' },
                        { icon: CreditCard, label: 'Ödeme Yöntemleri', sub: 'Mastercard •••• 1234', color: 'text-green-600', bg: 'bg-green-50' },
                    ].map((item, index) => (
                        <div key={index} className="flex items-center gap-4 p-4 border-b border-gray-50 last:border-0 hover:bg-gray-50 cursor-pointer transition-colors">
                            <div className={`w-10 h-10 ${item.bg} rounded-full flex items-center justify-center ${item.color}`}>
                                <item.icon size={20} />
                            </div>
                            <div className="flex-1">
                                <h3 className="font-bold text-gray-900 text-sm">{item.label}</h3>
                                <p className="text-[10px] text-gray-400">{item.sub}</p>
                            </div>
                            <ChevronRight size={18} className="text-gray-300" />
                        </div>
                    ))}
                </div>

                {/* Help Section */}
                <div className="bg-white rounded-2xl p-4 shadow-sm flex items-center gap-4 cursor-pointer hover:bg-gray-50 transition-colors">
                    <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-gray-600">
                        <HelpCircle size={20} />
                    </div>
                    <div className="flex-1">
                        <h3 className="font-bold text-gray-900 text-sm">Yardım & Destek</h3>
                        <p className="text-xs text-gray-500">Sıkça sorulan sorular</p>
                    </div>
                    <ChevronRight size={18} className="text-gray-300" />
                </div>

                {/* Order Analysis (Keep existing) */}
                <div className="bg-white rounded-2xl p-6 shadow-sm">
                    <h3 className="font-bold text-gray-900 mb-4 text-sm">Alışveriş Analizin</h3>
                    <div className="flex flex-wrap gap-2">
                        {['Smart Casual', 'L Beden', 'Nişantaşı', 'Spor Giyim', 'Siyah'].map((tag, i) => (
                            <span key={i} className="px-3 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[10px] font-bold text-gray-500 uppercase tracking-wide">
                                {tag}
                            </span>
                        ))}
                    </div>
                </div>
            </div>

            {/* Floating Sparkle Button */}
            <div className="fixed bottom-24 right-6 pointer-events-none">
                <button className="w-14 h-14 bg-indigo-600 rounded-full shadow-xl flex items-center justify-center text-white relative pointer-events-auto">
                    <Sparkles size={24} />
                    <span className="absolute top-0 right-0 w-3 h-3 bg-pink-500 rounded-full border-2 border-white"></span>
                </button>
            </div>

            {/* Settings Modal */}
            <AnimatePresence>
                {isSettingsOpen && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsSettingsOpen(false)}
                            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                        />

                        <motion.div
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            className="bg-white rounded-3xl w-full max-w-sm p-6 relative z-10 shadow-2xl"
                        >
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-xl font-bold text-gray-900">Bildirim & Konum</h2>
                                <button onClick={() => setIsSettingsOpen(false)} className="p-2 bg-gray-100 rounded-full hover:bg-gray-200">
                                    <X size={20} className="text-gray-600" />
                                </button>
                            </div>

                            <div className="space-y-4">
                                {/* Location Toggle */}
                                <div
                                    onClick={handleLocationToggle}
                                    className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100 cursor-pointer active:scale-95 transition-transform"
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                                            <Zap size={20} fill="currentColor" />
                                        </div>
                                        <div>
                                            <h3 className="font-bold text-gray-800">Konum Ayarı</h3>
                                            <p className="text-xs text-gray-500">{locationEnabled ? 'Açık' : 'Kapalı'}</p>
                                        </div>
                                    </div>
                                    {isLoading ? (
                                        <div className="w-8 h-8 rounded-full border-2 border-indigo-200 border-t-indigo-600 animate-spin" />
                                    ) : locationEnabled ? (
                                        <ToggleRight size={32} className="text-green-500" />
                                    ) : (
                                        <ToggleLeft size={32} className="text-gray-400" />
                                    )}
                                </div>

                                {/* Notification Toggle */}
                                <div
                                    onClick={() => setNotificationsEnabled(!notificationsEnabled)}
                                    className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100 cursor-pointer active:scale-95 transition-transform"
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center text-purple-600">
                                            <Settings size={20} />
                                        </div>
                                        <div>
                                            <h3 className="font-bold text-gray-800">Bildirim Ayarı</h3>
                                            <p className="text-xs text-gray-500">{notificationsEnabled ? 'Açık' : 'Kapalı'}</p>
                                        </div>
                                    </div>
                                    {notificationsEnabled ? (
                                        <ToggleRight size={32} className="text-green-500" />
                                    ) : (
                                        <ToggleLeft size={32} className="text-gray-400" />
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Confirmation Warning Modal */}
            <AnimatePresence>
                {showLocationWarning && (
                    <div className="fixed inset-0 z-[60] flex items-center justify-center px-6">
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="absolute inset-0 bg-black/80 backdrop-blur-md"
                        />

                        <motion.div
                            initial={{ y: 50, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            exit={{ y: 50, opacity: 0 }}
                            className="bg-white rounded-3xl w-full max-w-sm p-6 relative z-10 text-center shadow-2xl"
                        >
                            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4 text-red-500 shadow-sm">
                                <AlertTriangle size={32} />
                            </div>

                            <h3 className="text-lg font-bold text-gray-900 mb-2">Emin misin?</h3>
                            <p className="text-sm text-gray-600 mb-8 leading-relaxed">
                                Konumunu kapatırsan mağazaya geldiğinde indirimleri kaçırırsın, emin misin?
                            </p>

                            <div className="flex flex-col gap-3">
                                <button
                                    onClick={confirmDisableLocation}
                                    className="w-full py-3 bg-red-50 text-red-600 font-bold rounded-xl hover:bg-red-100 transition-colors"
                                >
                                    Evet, Konumu Kapat
                                </button>
                                <button
                                    onClick={() => {
                                        setShowLocationWarning(false);
                                        setIsSettingsOpen(true); // Re-open settings
                                    }}
                                    className="w-full py-3 bg-gray-900 text-white font-bold rounded-xl hover:bg-gray-800 transition-colors shadow-lg shadow-gray-200"
                                >
                                    Hayır, Konumu Kapatma
                                </button>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

        </div>
    );
}

// Helper for Location Badge Logic
function LocationBadge({ locationEnabled, userLocation, userAddress }) {
    if (!locationEnabled) {
        return (
            <div className="mb-6 flex items-center justify-center gap-2">
                <div className="px-3 py-1 rounded-full text-[10px] font-medium flex items-center gap-1 bg-red-500/10 text-red-400 border border-red-500/20">
                    <Zap size={10} fill="currentColor" />
                    Konum Kapalı
                </div>
            </div>
        );
    }

    if (!userLocation) {
        return (
            <div className="mb-6 flex items-center justify-center gap-2">
                <div className="px-3 py-1 rounded-full text-[10px] font-medium flex items-center gap-1 bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 animate-pulse">
                    <Zap size={10} fill="currentColor" />
                    Konum Alınıyor...
                </div>
            </div>
        );
    }

    return (
        <div className="mb-6 flex items-center justify-center gap-2">
            <div className="px-3 py-1 rounded-full text-[10px] font-medium flex items-center gap-1 bg-green-500/10 text-green-400 border border-green-500/20">
                <Zap size={10} fill="currentColor" />
                {userAddress ? userAddress : `Konum: ${userLocation.lat.toFixed(5)}, ${userLocation.lng.toFixed(5)}`}
            </div>
        </div>
    );
}

// Helper for Floating Button
function Sparkles({ size, className }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={className}
        >
            <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
        </svg>
    )
}
