import React, { useState, useEffect } from 'react';
import { Wifi, Signal, Battery } from 'lucide-react';

export default function StatusBar({ theme = 'light' }) {
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date());
        }, 1000);

        return () => clearInterval(timer);
    }, []);

    // Format time as HH:mm
    const formattedTime = time.toLocaleTimeString('tr-TR', {
        hour: '2-digit',
        minute: '2-digit'
    });

    const textColor = theme === 'dark' ? 'text-white' : 'text-gray-900';

    return (
        <div className={`w-full flex justify-between items-center px-6 py-2 absolute top-0 left-0 z-50 pointer-events-none ${textColor}`}>
            {/* Clock */}
            <span className="font-bold text-sm tracking-wide font-sans">
                {formattedTime}
            </span>

            {/* Status Icons */}
            <div className="flex items-center gap-2">
                <Signal size={16} fill="currentColor" className="opacity-90" />
                <Wifi size={16} className="opacity-90" />
                <div className="relative">
                    <Battery size={20} className="opacity-90" />
                    <div className={`absolute top-[6px] right-[3px] w-[10px] h-[8px] rounded-[1px] ${theme === 'dark' ? 'bg-white' : 'bg-gray-900'}`} />
                </div>
            </div>
        </div>
    );
}
