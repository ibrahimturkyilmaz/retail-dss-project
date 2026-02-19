import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchAddressFromCoords } from '../utils/geocoding';

const LocationContext = createContext();

export function LocationProvider({ children }) {
    const [location, setLocation] = useState(null); // { lat, lng }
    const [address, setAddress] = useState(null); // "District, City"
    const [locationEnabled, setLocationEnabled] = useState(false);
    const [permissionStatus, setPermissionStatus] = useState('prompt'); // granted, denied, prompt
    const [isLoading, setIsLoading] = useState(false);

    // İlk Yükleme - Kayıtlı durumu kontrol et veya varsayılan olarak izin iste
    // İlk Yükleme - Kayıtlı durumu kontrol et veya varsayılan olarak izin iste
    useEffect(() => {
        // Basit kontrol: Eğer konum daha önce açıldıysa, tekrar etkinleştirmeyi dene
        if (locationEnabled) {
            setIsLoading(true);
            const watchId = navigator.geolocation.watchPosition(
                async (position) => {
                    const { latitude, longitude } = position.coords;
                    setLocation({ lat: latitude, lng: longitude });
                    setIsLoading(false);
                    setPermissionStatus('granted');

                    // Adres verisini (Geocoding) çekme mantığı
                    try {
                        const addr = await fetchAddressFromCoords(latitude, longitude);
                        if (addr) setAddress(addr.short);
                    } catch (e) {
                        console.warn("Address fetch failed", e);
                    }
                },
                (error) => {
                    console.error("Location Error:", error);
                    setIsLoading(false);
                    // Zaman aşımında otomatik kapatma, sadece reddedilirse (deny) kapat
                    if (error.code === 1) {
                        setLocationEnabled(false);
                        setPermissionStatus('denied');
                    }
                },
                { enableHighAccuracy: true, timeout: 20000, maximumAge: 5000 }
            );
            return () => navigator.geolocation.clearWatch(watchId);
        } else {
            setLocation(null);
            setAddress(null);
            setIsLoading(false);
        }
    }, [locationEnabled]);

    const requestPermission = () => {
        if (!navigator.geolocation) {
            alert("Cihazınız konum servisini desteklemiyor.");
            return;
        }
        setIsLoading(true);

        const options = { enableHighAccuracy: true, timeout: 30000, maximumAge: 0 };

        // Helper specifically for the initial request
        const attemptLocation = (opts, isRetry = false) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    setLocation({ lat: latitude, lng: longitude }); // Set immediately
                    setLocationEnabled(true);
                    setPermissionStatus('granted');
                    setIsLoading(false);
                },
                (error) => {
                    if (!isRetry && (error.code === 3 || error.code === 2)) {
                        // Retry with low accuracy if timeout or position unavailable
                        console.warn("High accuracy failed, retrying with low accuracy...");
                        attemptLocation({ enableHighAccuracy: false, timeout: 30000, maximumAge: 0 }, true);
                    } else {
                        setLocationEnabled(false);
                        setPermissionStatus('denied');
                        setIsLoading(false);
                        if (error.code === 1) alert("Konum izni reddedildi. Lütfen tarayıcı ayarlarından izin verin.");
                        else if (error.code === 2) alert("Konum alınamadı. GPS kapalı olabilir.");
                        else if (error.code === 3) alert("Konum alma zaman aşımına uğradı. Lütfen açık bir alana geçin.");
                    }
                },
                opts
            );
        };

        attemptLocation(options);
    };



    return (
        <LocationContext.Provider value={{
            location,
            address,
            locationEnabled,
            setLocationEnabled,
            requestPermission,
            permissionStatus,
            isLoading
        }}>
            {children}
        </LocationContext.Provider>
    );
}

export const useLocation = () => useContext(LocationContext);
