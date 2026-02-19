export async function fetchAddressFromCoords(lat, lng) {
    try {
        const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
        // Use Backend Proxy to avoid CORS
        const response = await fetch(`${API_URL}/api/utils/proxy/reverse-geocode?lat=${lat}&lon=${lng}`);

        if (!response.ok) {
            throw new Error('Geocoding service unavailable');
        }

        const data = await response.json();

        // Extract relevant parts (City / District / Neighborhood)
        const address = data.address;

        const city = address.province || address.city || address.state || '';
        const district = address.town || address.district || address.county || '';
        const neighborhood = address.suburb || address.neighbourhood || address.quarter || '';

        // Format: City / District / Neighborhood
        // Filter out empty parts and join with " / "
        const parts = [city, district, neighborhood].filter(Boolean);
        const formattedShort = parts.length > 0 ? parts.join(' / ') : 'Bilinmeyen Konum';

        return {
            full: data.display_name,
            short: formattedShort,
            city,
            district,
            neighborhood
        };
    } catch (error) {
        console.error("Geocoding Error:", error);
        return null; // Fail gracefully
    }
}
