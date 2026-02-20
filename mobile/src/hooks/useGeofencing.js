import { useState, useEffect } from 'react';
import { calculateDistance } from '../utils/location';
import { useLocation } from '../context/LocationContext';
import { useUser } from '../context/UserContext';

export function useGeofencing(stores) {
    const { location, locationEnabled, address } = useLocation();
    const { user } = useUser();
    const [notification, setNotification] = useState(null);
    const [isSimulated, setIsSimulated] = useState(false);

    // Simulation Functions
    const simulateEnterRegion = async (storeId) => {
        console.log("Simulating Enter Region for Store:", storeId);

        if (!locationEnabled) {
            console.warn("Location services are disabled in context.");
            setNotification({
                title: "⚠️ Konum Gerekli",
                message: "Simülasyonu başlatmak için lütfen konum izni verin.",
                action: { label: "İzin İste", onClick: () => console.log("Requesting via button...") }
            });
            return;
        }

        const store = stores.find(s => s.id === storeId);
        if (!store) {
            console.error("Store not found in mock data:", storeId);
            return;
        }

        console.log("Found Store:", store.name, "at", store.lat, store.lng);
        setIsSimulated(true);

        // Immediate feedback so user knows something is happening
        setNotification({
            title: "🔍 Koordinatlar Gönderiliyor...",
            message: `${store.name} mağazasına yaklaştığınız simüle ediliyor...`,
            action: null
        });

        // Backend Call to Simulate & Trigger Email
        try {
            const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const customerId = user?.id || 32;

            console.log(`Calling backend: ${API_URL}/api/marketing/check-proximity for user ${customerId}`);

            const response = await fetch(`${API_URL}/api/marketing/check-proximity`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    lat: store.lat || 41.0522,
                    lon: store.lng || 28.9959,
                    customer_id: customerId
                })
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Backend response received:", data);

                if (data.notification) {
                    setNotification({
                        storeId: data.store,
                        title: `🔔 ${data.title}`,
                        message: data.message,
                        action: { label: "Kuponu Gör", onClick: () => alert(`Kupon Kodu: ${data.coupon_code}`) }
                    });
                } else {
                    setNotification({
                        title: "📍 Konum İletildi",
                        message: `Sistem yakında olduğunuzu biliyor fakat kampanya koşulları oluşmadı: ${data.reason || 'Bilinmiyor'}`,
                    });
                }
            } else {
                console.error("Backend Error Response:", response.status);
                setNotification({
                    title: "⚠️ Sunucu Hatası",
                    message: "Kampanya verileri alınamadı. Lütfen daha sonra tekrar deneyin.",
                });
            }
        } catch (error) {
            console.error("Simulation Fetch Error:", error);
            setNotification({
                title: "❌ Bağlantı Hatası",
                message: "Sunucuya ulaşılamıyor. İnternet bağlantınızı kontrol edin.",
            });
        }
    };

    const simulateInStore = () => {
        // Beacon simulation logic remains similar or can also call backend
        if (!locationEnabled) {
            setNotification({
                title: "⚠️ Uyarı",
                message: "Kullanıcının konumu kapalı.",
                action: null
            });
            return;
        }
        setIsSimulated(true);
        setNotification({
            title: "🤭 Duyduk ki Mağazamızdaymışsın!",
            message: "Beğendiğin ürünü şimdi uygulama üzerinden al, kasada sıra bekleme!",
            action: null
        });
    };

    // Real Loop for Geofencing - Backend Integration
    useEffect(() => {
        if (!locationEnabled || !location) {
            if (!locationEnabled) setNotification(null);
            return;
        }

        const checkBackendProximity = async () => {
            try {
                // Use environment variable for API URL, fallback to localhost for dev
                const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

                // Demo User ID (or 32 for 'kemal.yildiz')
                const customerId = user?.id || 32;

                const response = await fetch(`${API_URL}/api/marketing/check-proximity`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        lat: location.lat,
                        lon: location.lng,
                        customer_id: customerId
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.notification) {
                        setNotification({
                            storeId: data.store, // Using store name/id
                            title: data.title,
                            message: data.message,
                            action: { label: "Kuponu Gör", onClick: () => alert(`Kupon Kodu: ${data.coupon_code}`) }
                        });
                    }
                }
            } catch (error) {
                console.error("Geofence Check Error:", error);
            }
        };

        // Check every 30 seconds to avoid spamming the API
        const intervalId = setInterval(checkBackendProximity, 30000);

        // Initial Check
        checkBackendProximity();

        return () => clearInterval(intervalId);

    }, [location, locationEnabled, user]);

    return {
        // We pass through location/address for convenience if needed, but components can also get them from context directly
        // Keeping them here minimizes breakage if App.jsx expects them from this hook
        location,
        address,
        notification,
        simulateEnterRegion,
        simulateInStore,
        dismissNotification: () => setNotification(null)
    };
}
