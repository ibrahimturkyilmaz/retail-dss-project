export async function fetchAddressFromCoords(lat, lng) {
    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`, {
            headers: {
                'User-Agent': 'RetailAppDemo/1.0' // Nice to have for OSM
            }
        });

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
