import React from 'react';
import { BellIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';

const Header = ({ title }) => {
    return (
        <header className="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10 transition-colors">

            {/* Page Title */}
            <div>
                <h2 className="text-2xl font-bold text-slate-800 tracking-tight">{title}</h2>
                <p className="text-xs text-slate-500 mt-1">Sistem Durumu: <span className="text-green-500 font-medium">Aktif</span></p>
            </div>

            {/* Actions Area */}
            <div className="flex items-center space-x-6">

                {/* Search Bar */}
                <div className="relative hidden md:block group">
                    <MagnifyingGlassIcon className="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 group-hover:text-blue-500 transition-colors" />
                    <input
                        type="text"
                        placeholder="Ara..."
                        className="pl-10 pr-4 py-2 bg-slate-100 border-none rounded-full text-sm text-slate-700 focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all w-64"
                    />
                </div>

                {/* Notifications */}
                <button className="relative p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-500 hover:text-slate-700">
                    <BellIcon className="w-6 h-6" />
                    <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
                </button>
            </div>
        </header>
    );
};

export default Header;
