import React from 'react';
import { NavLink } from 'react-router-dom';
import { NAVIGATION_ITEMS, BOTTOM_NAVIGATION_ITEMS } from '../constants/navigation';

const Sidebar = () => {
    return (
        <div className="flex flex-col w-64 h-screen bg-slate-900 text-white border-r border-slate-800 transition-all duration-300 ease-in-out">
            {/* Logo Area */}
            <div className="flex items-center justify-center h-20 border-b border-slate-800">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    Retail DSS
                </h1>
            </div>

            {/* Main Navigation */}
            <nav className="flex-1 overflow-y-auto py-4">
                <ul className="space-y-2 px-3">
                    {NAVIGATION_ITEMS.map((item) => (
                        <li key={item.path}>
                            <NavLink
                                to={item.path}
                                className={({ isActive }) =>
                                    // Modern hover & active states with glassmorphism feel
                                    `flex items-center px-4 py-3 rounded-xl transition-all duration-200 group
                  ${isActive
                                        ? 'bg-blue-600/20 text-blue-400 font-medium shadow-[0_0_15px_rgba(59,130,246,0.2)]'
                                        : 'text-slate-400 hover:bg-slate-800/50 hover:text-white'
                                    }`
                                }
                            >
                                <item.icon className="w-6 h-6 mr-3" />
                                <span className="text-sm tracking-wide">{item.name}</span>
                            </NavLink>
                        </li>
                    ))}
                </ul>
            </nav>

            {/* Bottom Actions */}
            <div className="p-4 border-t border-slate-800">
                <ul className="space-y-2">
                    {BOTTOM_NAVIGATION_ITEMS.map((item) => (
                        <li key={item.path}>
                            <NavLink
                                to={item.path}
                                className={({ isActive }) =>
                                    `flex items-center px-4 py-3 rounded-xl transition-all duration-200
                  ${isActive
                                        ? 'bg-slate-800 text-white'
                                        : 'text-slate-500 hover:bg-slate-800/30 hover:text-slate-300'
                                    }`
                                }
                            >
                                <item.icon className="w-5 h-5 mr-3" />
                                <span className="text-sm font-medium">{item.name}</span>
                            </NavLink>
                        </li>
                    ))}
                </ul>
                <div className="mt-4 flex items-center px-4 py-2">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-green-400 to-blue-500 flex items-center justify-center text-xs font-bold text-white shadow-lg">
                        IT
                    </div>
                    <div className="ml-3">
                        <p className="text-sm font-medium text-white">İbrahim T.</p>
                        <p className="text-xs text-slate-500">Yönetici</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
