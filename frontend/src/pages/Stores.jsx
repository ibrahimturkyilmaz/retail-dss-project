import React, { useState } from 'react';
import { useStores } from '../hooks/useStores';
import StoreMap from '../components/StoreMap';
import { FixedSizeList as List } from 'react-window';
import AutoSizer from 'react-virtualized-auto-sizer';
import { MapPinIcon, BuildingStorefrontIcon } from '@heroicons/react/24/outline';

const Stores = () => {
    const { data: stores, isLoading, error } = useStores();
    const [selectedStore, setSelectedStore] = useState(null);

    if (isLoading) return <div className="p-10 text-center text-slate-500">Mağazalar yükleniyor...</div>;
    if (error) return <div className="p-10 text-center text-red-500">Bir hata oluştu: {error.message}</div>;

    // Row component for react-window
    const Row = ({ index, style }) => {
        const store = stores[index];
        const isSelected = selectedStore?.id === store.id;

        return (
            <div style={style} className="px-2 py-2">
                <div
                    onClick={() => setSelectedStore(store)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all duration-200 flex items-center justify-between
                ${isSelected
                            ? 'bg-blue-50 border-blue-500 shadow-md transform scale-[1.01]'
                            : 'bg-white border-slate-100 hover:border-blue-200 hover:shadow-sm'
                        }`}
                >
                    <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded-lg ${store.store_type === 'HUB' ? 'bg-purple-100 text-purple-600' : 'bg-blue-100 text-blue-600'}`}>
                            <BuildingStorefrontIcon className="w-5 h-5" />
                        </div>
                        <div>
                            <h4 className="font-semibold text-slate-800 text-sm">{store.name}</h4>
                            <p className="text-xs text-slate-500">{store.store_type}</p>
                        </div>
                    </div>

                    <div className="text-right">
                        <div className={`text-xs font-bold px-2 py-1 rounded-full inline-block mb-1
                 ${store.stock < store.safety_stock ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                            {store.stock} Adet
                        </div>
                        <p className="text-[10px] text-slate-400">Stok</p>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="h-[calc(100vh-140px)] flex flex-col md:flex-row gap-6">
            {/* Left Side: Virtualized List */}
            <div className="w-full md:w-1/3 bg-white rounded-2xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
                <div className="p-4 border-b border-slate-100 bg-slate-50/50">
                    <h2 className="text-lg font-bold text-slate-800">Mağazalar ({stores?.length})</h2>
                    <p className="text-xs text-slate-500 mt-1">Hızlı erişim ve stok durumu.</p>
                </div>

                <div className="flex-1">
                    <AutoSizer>
                        {({ height, width }) => (
                            <List
                                height={height}
                                width={width}
                                itemCount={stores.length}
                                itemSize={90} // Height of each row
                            >
                                {Row}
                            </List>
                        )}
                    </AutoSizer>
                </div>
            </div>

            {/* Right Side: Map */}
            <div className="w-full md:w-2/3 bg-white rounded-2xl shadow-sm border border-slate-200 p-1 relative overflow-hidden">
                <StoreMap stores={stores} selectedStore={selectedStore} />

                {/* Floating Info Overlay */}
                <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm p-3 rounded-lg shadow-lg z-[400] text-xs max-w-xs border border-slate-200">
                    <h4 className="font-bold text-slate-800 mb-1">Harita Bilgisi</h4>
                    <p className="text-slate-500">Mavi çemberler HUB (Ana Depo) etki alanını gösterir. Kırmızı işaretler riskli stok seviyelerini ifade eder.</p>
                </div>
            </div>
        </div>
    );
};

export default Stores;
