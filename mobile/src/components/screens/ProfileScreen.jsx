import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Settings, CreditCard, Bell, LogOut, ChevronRight, Package, MapPin, Heart, Shield, Navigation, ToggleLeft, ToggleRight, Mail } from 'lucide-react';
import { useUser } from '../../context/UserContext';
import { useLocation } from '../../context/LocationContext';
import { clsx } from 'clsx';

export default function ProfileScreen({ notificationsEnabled, setNotificationsEnabled }) {
    const { user, logout } = useUser();
    const { locationEnabled, setLocationEnabled, requestPermission, address } = useLocation();

    if (!user) return null;

    const handleLocationToggle = () => {
        if (locationEnabled) {
            setLocationEnabled(false);
            localStorage.setItem('retail-app-location-allowed', 'false');
        } else {
            requestPermission();
        }
    };

    const menuItems = [
        { icon: <Package size={20} />, label: 'Siparişlerim', value: '12 Aktif' },
        { icon: <Heart size={20} />, label: 'Favorilerim', value: '5 Ürün' },
        { icon: <MapPin size={20} />, label: 'Adreslerim', value: '2 Kayıtlı' },
        { icon: <CreditCard size={20} />, label: 'Ödeme Yöntemleri', value: '**42' },
    ];

    const settingsItems = [
        {
            icon: <Navigation size={20} />,
            label: 'Konum Servisi',
            type: 'toggle',
            state: locationEnabled,
            toggle: handleLocationToggle,
            color: 'text-blue-600',
            bg: 'bg-blue-50'
        },
        {
            icon: <Bell size={20} />,
            label: 'Bildirimler',
            type: 'toggle',
            state: notificationsEnabled,
            toggle: () => setNotificationsEnabled(!notificationsEnabled),
            color: 'text-purple-600',
            bg: 'bg-purple-50'
        },
        { icon: <Shield size={20} />, label: 'Gizlilik ve Güvenlik', type: 'link', color: 'text-slate-600', bg: 'bg-slate-100' },
        { icon: <Settings size={20} />, label: 'Uygulama Ayarları', type: 'link', color: 'text-slate-600', bg: 'bg-slate-100' },
    ];

    return (
        <div className="min-h-screen bg-slate-50 pb-24 relative">
            {/* Header Background */}
            <div className="bg-slate-900 h-64 relative overflow-hidden rounded-b-[3rem]">
                <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500 rounded-full mix-blend-overlay filter blur-3xl opacity-20 animate-blob"></div>
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-teal-500 rounded-full mix-blend-overlay filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
            </div>

            <div className="px-6 -mt-48 relative z-10">
                {/* Profile Header */}
                <div className="flex flex-col items-center mb-6">
                    <div className="relative mb-4 group cursor-pointer">
                        <div className="w-28 h-28 rounded-full p-1 bg-gradient-to-tr from-indigo-500 to-teal-500 shadow-xl shadow-indigo-500/20">
                            <div className="w-full h-full bg-white rounded-full p-1">
                                <img
                                    src="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=400&auto=format&fit=crop&q=80"
                                    alt="Profile"
                                    className="w-full h-full rounded-full object-cover transition-transform duration-500 group-hover:scale-110"
                                />
                            </div>
                        </div>
                        <div className="absolute bottom-0 right-2 bg-indigo-600 text-white rounded-full p-2 border-4 border-slate-900 shadow-md">
                            <Settings size={14} />
                        </div>
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-1 font-heading tracking-tight">{user.name}</h1>
                    <p className="text-indigo-200 font-medium">✨ Gold Üye</p>
                </div>

                {/* Live Location Display Card */}
                {locationEnabled && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-4 mb-8 flex items-center gap-3 shadow-lg"
                    >
                        <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-300 animate-pulse">
                            <Navigation size={20} fill="currentColor" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-indigo-200 text-xs font-bold uppercase tracking-wide mb-0.5">Mevcut Konum</p>
                            <p className="text-white font-medium truncate text-sm">
                                {address ? address.short : 'Konum alınıyor...'}
                            </p>
                        </div>
                    </motion.div>
                )}

                {/* Stats Card */}
                {!locationEnabled && (
                    <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-3xl p-6 mb-8 shadow-xl grid grid-cols-3 gap-4 text-center">
                        <div>
                            <span className="block text-2xl font-bold text-white mb-1 font-heading">1500</span>
                            <span className="text-xs text-indigo-100 uppercase tracking-widest font-semibold">Puan</span>
                        </div>
                        <div className="border-x border-white/10">
                            <span className="block text-2xl font-bold text-white mb-1 font-heading">12</span>
                            <span className="text-xs text-indigo-100 uppercase tracking-widest font-semibold">Sipariş</span>
                        </div>
                        <div>
                            <span className="block text-2xl font-bold text-white mb-1 font-heading">4</span>
                            <span className="text-xs text-indigo-100 uppercase tracking-widest font-semibold">Kupon</span>
                        </div>
                    </div>
                )}

                {/* Menu Grid */}
                <h3 className="text-slate-900 font-bold mb-4 font-heading text-lg px-2">Hesabım</h3>
                <div className="bg-white rounded-[2rem] p-2 shadow-sm border border-slate-100 mb-8">
                    {menuItems.map((item, index) => (
                        <button key={index} className="w-full flex items-center justify-between p-4 hover:bg-slate-50 rounded-2xl transition-colors group">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 rounded-xl bg-slate-50 text-slate-600 flex items-center justify-center group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                                    {item.icon}
                                </div>
                                <span className="font-semibold text-slate-700 font-heading">{item.label}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                {item.value && <span className="text-sm font-medium text-slate-400">{item.value}</span>}
                                <ChevronRight size={18} className="text-slate-300 group-hover:text-indigo-400" />
                            </div>
                        </button>
                    ))}
                </div>

                {/* Settings Section */}
                <h3 className="text-slate-900 font-bold mb-4 font-heading text-lg px-2">Ayarlar</h3>
                <div className="bg-white rounded-[2rem] p-2 shadow-sm border border-slate-100 mb-8">
                    {settingsItems.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-4 hover:bg-slate-50 rounded-2xl transition-colors">
                            <div className="flex items-center gap-4">
                                <div className={clsx("w-10 h-10 rounded-xl flex items-center justify-center", item.bg, item.color)}>
                                    {item.icon}
                                </div>
                                <span className="font-semibold text-slate-700 font-heading">{item.label}</span>
                            </div>
                            {item.type === 'toggle' ? (
                                <button
                                    onClick={item.toggle}
                                    className={clsx(
                                        "w-12 h-7 rounded-full transition-colors relative",
                                        item.state ? "bg-indigo-600" : "bg-slate-200"
                                    )}
                                >
                                    <div className={clsx(
                                        "w-5 h-5 bg-white rounded-full absolute top-1 transition-all shadow-sm",
                                        item.state ? "left-6" : "left-1"
                                    )} />
                                </button>
                            ) : (
                                <ChevronRight size={18} className="text-slate-300" />
                            )}
                        </div>
                    ))}
                </div>

                {/* Logout Button */}
                <button
                    onClick={logout}
                    className="w-full bg-red-50 text-red-600 rounded-2xl py-4 font-bold flex items-center justify-center gap-2 hover:bg-red-100 transition-colors mb-6 shadow-sm border border-red-100"
                >
                    <LogOut size={20} />
                    Çıkış Yap
                </button>

                <p className="text-center text-slate-400 text-xs font-medium pb-8">
                    Version 1.2.0 • Build 2024.04
                </p>
            </div>
        </div>
    );
}
