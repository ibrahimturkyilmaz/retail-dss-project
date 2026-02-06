import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Circle, Polyline } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet Default Icon Issue in Vite/Webpack
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconUrl: markerIcon,
    iconRetinaUrl: markerIcon2x,
    shadowUrl: markerShadow,
});

// Component to recenter map when selected store changes
const MapRecenter = ({ lat, lon }) => {
    const map = useMap();
    useEffect(() => {
        if (lat && lon) {
            map.flyTo([lat, lon], 13);
        }
    }, [lat, lon, map]);
    return null;
};

const StoreMap = ({ stores, selectedStore, activeTransfer }) => {
    // İstanbul merkezli varsayılan konum
    const defaultCenter = [41.0082, 28.9784];

    return (
        <MapContainer center={defaultCenter} zoom={10} className="w-full h-full rounded-2xl z-0">
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {selectedStore && <MapRecenter lat={selectedStore.lat} lon={selectedStore.lon} />}

            {/* Transfer Hattı Animasyonu (Varsa) */}
            {activeTransfer && (
                <Polyline
                    positions={[
                        [activeTransfer.source.lat, activeTransfer.source.lon],
                        [activeTransfer.target.lat, activeTransfer.target.lon]
                    ]}
                    color="#3b82f6"
                    weight={4}
                    dashArray="10, 10"
                    className="animate-dash" // Custom CSS animation needed
                />
            )}

            {stores.map((store) => (
                <React.Fragment key={store.id}>
                    <Marker position={[store.lat, store.lon]}>
                        <Popup>
                            <div className="p-1">
                                <h3 className="font-bold text-gray-800">{store.name}</h3>
                                <p className="text-xs text-gray-500">{store.store_type}</p>
                                <div className="mt-2 flex items-center space-x-2">
                                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${store.risk_status === 'High Gap' ? 'bg-red-100 text-red-600' :
                                        store.risk_status === 'Low Stock' ? 'bg-orange-100 text-orange-600' :
                                            'bg-green-100 text-green-600'
                                        }`}>
                                        {store.risk_status}
                                    </span>
                                    <span className="text-xs font-bold text-slate-700">Stok: {store.stock}</span>
                                </div>
                            </div>
                        </Popup>
                    </Marker>

                    {/* Circle for Hubs or Danger zones */}
                    {(store.store_type === 'HUB' || store.store_type === 'CENTER') && (
                        <Circle
                            center={[store.lat, store.lon]}
                            radius={store.store_type === 'CENTER' ? 8000 : 4000}
                            pathOptions={{
                                color: store.store_type === 'CENTER' ? 'purple' : 'blue',
                                fillColor: store.store_type === 'CENTER' ? 'purple' : 'blue',
                                fillOpacity: 0.1
                            }}
                        />
                    )}
                </React.Fragment>
            ))}
        </MapContainer>
    );
};

export default StoreMap;
