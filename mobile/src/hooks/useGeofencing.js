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
    const simulateEnterRegion = (storeId) => {
        if (!locationEnabled) {
            setNotification({
                title: "⚠️ Uyarı",
                message: "Kullanıcının konumu kapalı, bildirim gönderilemiyor.",
                action: { label: "Ayarları Aç", onClick: () => console.log("Open settings...") }
            });
            return;
        }
        setIsSimulated(true);
        const store = stores.find(s => s.id === storeId);
        if (!store) return;

        setNotification({
            title: "📍 150m Yakınlardasınız!",
            message: "Sepetinizde unuttuğunuz 'Vintage Ceket' Nişantaşı mağazamızda stokta! Denemek için harika bir zaman.",
            action: { label: "Mağazayı Gör", onClick: () => console.log("Navigating to store...") }
        });
    };

    const simulateInStore = () => {
        if (!locationEnabled) {
            setNotification({
                title: "⚠️ Uyarı",
                message: "Kullanıcının konumu kapalı, bildirim gönderilemiyor.",
                action: null
            });
            return;
        }
        setIsSimulated(true);
        setNotification({
            title: "🤭 Duyduk ki Mağazamızdaymışsın!",
            message: "Beğendiğin ürünü şimdi uygulama üzerinden al, kasada sıra bekleme ve anında %10 indirim + 2X Puan kazan!",
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
