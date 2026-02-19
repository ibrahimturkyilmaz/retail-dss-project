import React from 'react';
import { Home, ShoppingBag, User, Heart, ShoppingCart } from 'lucide-react';
import { clsx } from 'clsx';
import { motion } from 'framer-motion';

export default function BottomNav({ activeTab, setActiveTab }) {
    const tabs = [
        { id: 'home', icon: Home, label: 'Home' },
        { id: 'shop', icon: ShoppingBag, label: 'Shop' },
        { id: 'favorites', icon: Heart, label: 'Favs' },
        { id: 'cart', icon: ShoppingCart, label: 'Cart' },
        { id: 'profile', icon: User, label: 'Profile' }
    ];

    return (
        <div className="fixed bottom-0 left-0 w-full bg-white border-t border-gray-100 pb-safe pt-1 px-1 shadow-[0_-5px_20px_rgba(0,0,0,0.03)] z-50 h-[65px] flex items-end">
            <div className="flex justify-between items-end max-w-md mx-auto relative w-full h-full">
                {tabs.map((tab) => {
                    const isActive = activeTab === tab.id;
                    const Icon = tab.icon;

                    return (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className="group flex flex-col items-center justify-center w-1/5 h-full relative touch-manipulation pb-1"
                        >
                            <div className={clsx(
                                "relative transition-all duration-300 ease-spring",
                                isActive ? "-translate-y-2" : ""
                            )}>
                                {/* Active Indicator Background */}
                                {isActive && (
                                    <motion.div
                                        layoutId="navBlob"
                                        className="absolute -inset-3 bg-indigo-50 rounded-2xl -z-10"
                                        initial={false}
                                        transition={{ type: "spring", stiffness: 400, damping: 30 }}
                                    />
                                )}

                                {/* Icon with Stroke Animation */}
                                <div className={clsx(
                                    "relative p-1 rounded-xl transition-colors duration-200",
                                    isActive ? "text-indigo-600" : "text-gray-400 group-hover:text-gray-600"
                                )}>
                                    <Icon
                                        size={24}
                                        strokeWidth={isActive ? 2.5 : 2}
                                        className="relative z-10"
                                    />

                                    {/* Stroke "Drawing" Animation Effect */}
                                    {isActive && (
                                        <motion.svg
                                            className="absolute inset-0 w-full h-full text-indigo-600 overflow-visible pointer-events-none"
                                            viewBox="0 0 24 24"
                                        >
                                            {/* Abstract circle or underline decoration that draws itself */}
                                            {/* Ideally we would animate the stroke of the Icon itself, but Lucide icons are components. 
                                               We can simulate a "sparkle" or "redraw" by animating a surrounding element or opacity. 
                                               Here we animate a small dot indicator below. */}
                                        </motion.svg>
                                    )}
                                </div>
                            </div>

                            <span className={clsx(
                                "text-[10px] font-bold mt-1 transition-all duration-300 absolute -bottom-1",
                                isActive ? "opacity-100 translate-y-0 text-indigo-600" : "opacity-0 translate-y-2"
                            )}>
                                {tab.label}
                            </span>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
