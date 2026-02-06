import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { Outlet, useLocation } from 'react-router-dom';
import { NAVIGATION_ITEMS } from '../constants/navigation';

const DashboardLayout = () => {
    const location = useLocation();

    // Find current page title based on path
    const currentRoute = NAVIGATION_ITEMS.find(item => item.path === location.pathname);
    const pageTitle = currentRoute ? currentRoute.name : 'Dashboard';

    return (
        <div className="flex h-screen bg-slate-50 font-sans antialiased selection:bg-blue-500 selection:text-white overflow-hidden">
            {/* Sidebar - Fixed width */}
            <Sidebar />

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
                {/* Header */}
                <Header title={pageTitle} />

                {/* Scrollable Content */}
                <main className="flex-1 overflow-y-auto p-8 scroll-smooth hover:scroll-auto">
                    <div className="max-w-7xl mx-auto animate-in fade-in duration-500 slide-in-from-bottom-4">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;
