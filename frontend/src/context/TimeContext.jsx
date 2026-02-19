import React, { createContext, useContext, useState, useEffect } from 'react';

const TimeContext = createContext();

export const useTime = () => useContext(TimeContext);

export const TimeProvider = ({ children }) => {
    // Varsayılan: Şu anki zaman
    const [virtualTime, setVirtualTime] = useState(new Date());
    const [canZReport, setCanZReport] = useState(false);

    // İş Kuralları: Saat 19:00'dan sonra Z-Raporu alınabilir.
    const CLOSING_HOUR = 19;

    useEffect(() => {
        const checkBusinessRules = () => {
            const currentHour = virtualTime.getHours();
            // Eğer saat 19:00 veya sonrasıysa Z-Raporu butonu açılır.
            if (currentHour >= CLOSING_HOUR) {
                setCanZReport(true);
            } else {
                setCanZReport(false);
            }
        };
        checkBusinessRules();
    }, [virtualTime]);

    const jumpTime = (hours) => {
        const newTime = new Date(virtualTime);
        newTime.setHours(newTime.getHours() + hours);
        setVirtualTime(newTime);
    };

    const resetTime = () => {
        setVirtualTime(new Date());
    };

    const value = {
        virtualTime,
        canZReport,
        jumpTime,
        resetTime,
        CLOSING_HOUR
    };

    return (
        <TimeContext.Provider value={value}>
            {children}
        </TimeContext.Provider>
    );
};
