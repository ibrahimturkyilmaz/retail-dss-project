import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchAddressFromCoords } from '../utils/geocoding';

const LocationContext = createContext();

export function LocationProvider({ children }) {
    const [location, setLocation] = useState(null); // { lat, lng }
    const [address, setAddress] = useState(null); // "District, City"
    const [locationEnabled, setLocationEnabled] = useState(false);
    const [permissionStatus, setPermissionStatus] = useState('prompt'); // granted, denied, prompt
    const [isLoading, setIsLoading] = useState(false);

    // 1. Uygulama açılışında kontrol: Daha önce izin verilmiş mi?
    useEffect(() => {
        const checkPermission = async () => {
            // Önce LocalStorage'a bak: Kullanıcı daha önce "Evet" demiş mi?
            const savedPreference = localStorage.getItem('retail-app-location-allowed');

            if (savedPreference === 'true') {
                // Tarayıcı seviyesinde izin durumunu kontrol et
                if (navigator.permissions && navigator.permissions.query) {
                    try {
                        const result = await navigator.permissions.query({ name: 'geolocation' });
                        if (result.state === 'granted') {
                            // İzin zaten varsa direkt başlat
                            setLocationEnabled(true);
                            setPermissionStatus('granted');
                        } else if (result.state === 'prompt') {
                            // Henüz sorulmamış ama biz "hatırla" demişiz -> Otomatik iste
                            requestPermission();
                        }
                    } catch (error) {
                        console.warn("Permission query failed", error);
                    }
                } else {
                    // Eski tarayıcılar için direkt dene
                    setLocationEnabled(true);
                }
            }
        };

        checkPermission();
    }, []);

    // 2. Konum izni açıldığında çalışacak watcher
    useEffect(() => {
        let watchId;

        if (locationEnabled) {
            setIsLoading(true);

            if (!navigator.geolocation) {
                alert("Tarayıcınız konum servisini desteklemiyor.");
                setIsLoading(false);
                return;
            }

            watchId = navigator.geolocation.watchPosition(
                async (position) => {
                    const { latitude, longitude } = position.coords;

                    // Gereksiz render'ı önlemek için sadece değişim varsa güncelle (basit bir threshold ile)
                    setLocation(prev => {
                        if (prev && prev.lat === latitude && prev.lng === longitude) return prev;
                        return { lat: latitude, lng: longitude };
                    });

                    setIsLoading(false);
                    setPermissionStatus('granted');

                    // Başarılı olduğunda tercihi kaydet
                    localStorage.setItem('retail-app-location-allowed', 'true');

                    // Adres verisini (Geocoding) çekme
                    try {
                        const addr = await fetchAddressFromCoords(latitude, longitude);
                        if (addr) setAddress(addr);
                    } catch (e) {
                        console.warn("Address fetch failed", e);
                    }
                },
                (error) => {
                    console.error("Location Error:", error);
                    setIsLoading(false);

                    if (error.code === 1) { // PERMISSION_DENIED
                        setLocationEnabled(false);
                        setPermissionStatus('denied');
                        localStorage.setItem('retail-app-location-allowed', 'false'); // Reddedildiyse tercihi güncelle
                    }
                },
                { enableHighAccuracy: true, timeout: 20000, maximumAge: 5000 }
            );
        } else {
            // Kapatıldıysa state'i temizle
            setLocation(null);
            setAddress(null);
            setIsLoading(false);
        }

        return () => {
            if (watchId) navigator.geolocation.clearWatch(watchId);
        };
    }, [locationEnabled]);

    const requestPermission = () => {
        if (!navigator.geolocation) {
            alert("Cihazınız konum servisini desteklemiyor.");
            return;
        }

        setIsLoading(true);
        const options = { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 };

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                setLocation({ lat: latitude, lng: longitude });
                setLocationEnabled(true);
                setPermissionStatus('granted');
                localStorage.setItem('retail-app-location-allowed', 'true'); // İzin verildi olarak kaydet
                setIsLoading(false);
            },
            (error) => {
                console.warn("Initial location request failed:", error);

                // Hata olsa bile retry veya manuel işlem için state güncelle
                if (error.code === 1) { // Kullanıcı reddetti
                    setPermissionStatus('denied');
                    localStorage.setItem('retail-app-location-allowed', 'false');
                }

                setLocationEnabled(false);
                setIsLoading(false);

                // Sadece kullanıcı butona bastıysa uyarı göster (otomatik kontrol değilse)
                // Bu örnekte requestPermission genelde kullanıcı tetiklemesi ile çağrılır
                if (error.code === 1) alert("Konum izni reddedildi. Lütfen tarayıcı ayarlarından izin verin.");
            },
            options
        );
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
