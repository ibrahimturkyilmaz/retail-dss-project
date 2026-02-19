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

        // Extract relevant parts (District / City)
        // Nominatim returns variable fields (city, town, village, county, state)
        const address = data.address;

        const district = address.suburb || address.neighbourhood || address.district || address.county || '';
        const city = address.city || address.town || address.province || address.state || '';

        return {
            full: data.display_name,
            short: district && city ? `${district}, ${city}` : (city || district || 'Bilinmeyen Konum'),
            district,
            city
        };
    } catch (error) {
        console.error("Geocoding Error:", error);
        return null; // Fail gracefully
    }
}
