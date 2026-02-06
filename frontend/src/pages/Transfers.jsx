import React, { useState } from 'react';
import { useTransfers } from '../hooks/useTransfers';
import { useStores } from '../hooks/useStores';
import StoreMap from '../components/StoreMap';
import { ArrowRightIcon, TruckIcon, LightBulbIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

const XAICard = ({ recommendation, onExecute, isExecuting }) => {
    const { source, target, product, amount, xai_explanation } = recommendation;
    const [expanded, setExpanded] = useState(false);

    return (
        <div
            className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-all mb-4 group"
            onMouseEnter={() => matchMedia('(min-width: 768px)').matches && setExpanded(true)}
            onMouseLeave={() => setExpanded(false)}
        >
            {/* Header */}
            <div className="flex justify-between items-start mb-3">
                <div className="flex items-center space-x-2">
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded-md">
                        {xai_explanation.score}% Acil
                    </span>
                    <h3 className="text-sm font-semibold text-slate-800">{product}</h3>
                </div>
                <div className="text-right">
                    <span className="text-lg font-bold text-slate-900">{amount} Adet</span>
                </div>
            </div>

            {/* Route */}
            <div className="flex items-center justify-between bg-slate-50 p-3 rounded-lg border border-slate-100 mb-3">
                <div className="text-left">
                    <p className="text-xs text-slate-400">Kaynak</p>
                    <p className="text-sm font-medium text-slate-700">{source.name}</p>
                    <span className="text-[10px] bg-slate-200 px-1 rounded text-slate-500">{source.type}</span>
                </div>
                <ArrowRightIcon className="w-5 h-5 text-slate-300" />
                <div className="text-right">
                    <p className="text-xs text-slate-400">Hedef</p>
                    <p className="text-sm font-medium text-slate-700">{target.name}</p>
                    <span className="text-[10px] bg-slate-200 px-1 rounded text-slate-500">{target.type}</span>
                </div>
            </div>

            {/* XAI Explanation (Always Visible Summary) */}
            <div className="flex items-start space-x-2 mb-3">
                <LightBulbIcon className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                <p className="text-xs text-slate-600 italic">
                    {xai_explanation.summary}
                </p>
            </div>

            {/* Detailed Reasons (Expandable) */}
            {expanded && (
                <div className="mb-4 animate-in fade-in slide-in-from-top-1 duration-200">
                    <ul className="space-y-1">
                        {xai_explanation.reasons.map((reason, idx) => (
                            <li key={idx} className="text-xs text-slate-500 flex items-center">
                                <span className="w-1 h-1 bg-slate-300 rounded-full mr-2"></span>
                                {reason}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Action Button */}
            <button
                onClick={() => onExecute(recommendation)}
                disabled={isExecuting}
                className="w-full flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {isExecuting ? (
                    <span>İşleniyor...</span>
                ) : (
                    <>
                        <TruckIcon className="w-4 h-4" />
                        <span>Transferi Onayla</span>
                    </>
                )}
            </button>
        </div>
    );
};

const Transfers = () => {
    const { recommendations, isLoading, executeTransfer, isExecuting } = useTransfers();
    const { data: stores } = useStores(); // Harita için mağazaları da çekelim
    const [hoveredTransfer, setHoveredTransfer] = useState(null);

    // Merge recommendation logic to find lat/lon for map animation
    // We need to match store IDs from recommendations with full store objects (which have lat/lon)
    const getActiveTransferData = () => {
        if (!hoveredTransfer || !stores) return null;

        const source = stores.find(s => s.id === hoveredTransfer.source.id);
        const target = stores.find(s => s.id === hoveredTransfer.target.id);

        if (source && target) {
            return { source, target };
        }
        return null;
    };

    if (isLoading) return <div className="p-10 text-center">Yükleniyor...</div>;

    return (
        <div className="h-[calc(100vh-140px)] flex gap-6">
            {/* Left: Recommendation List */}
            <div className="w-1/3 flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                    <div>
                        <h2 className="text-lg font-bold text-slate-800">Transfer Önerileri</h2>
                        <span className="text-xs text-slate-500">Yapay zeka destekli stok dengeleme.</span>
                    </div>
                    <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded-full">
                        {recommendations?.length || 0} Öneri
                    </span>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {recommendations?.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-full text-center text-slate-400">
                            <CheckCircleIcon className="w-12 h-12 mb-2 text-green-500" />
                            <p>Tüm stoklar dengeli!</p>
                            <p className="text-xs">Şu an için transfer önerisi bulunmuyor.</p>
                        </div>
                    ) : (
                        recommendations?.map((rec) => (
                            <div
                                key={rec.transfer_id}
                                onMouseEnter={() => setHoveredTransfer(rec)}
                                onMouseLeave={() => setHoveredTransfer(null)}
                            >
                                <XAICard
                                    recommendation={rec}
                                    onExecute={executeTransfer}
                                    isExecuting={isExecuting}
                                />
                            </div>
                        ))
                    )}
                </div>
            </div>

            {/* Right: Map */}
            <div className="w-2/3 bg-white rounded-2xl shadow-sm border border-slate-200 p-1 relative">
                {stores && (
                    <StoreMap
                        stores={stores}
                        activeTransfer={getActiveTransferData()}
                    />
                )}

                {/* Legend */}
                <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur p-3 rounded-lg shadow border border-slate-200 z-[400] text-xs">
                    <div className="flex items-center space-x-2 mb-1">
                        <span className="w-3 h-3 rounded-full bg-purple-500 opacity-20 border border-purple-500"></span>
                        <span>Merkez Depo Alanı</span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <span className="w-3 h-0.5 bg-blue-500 border-t border-dashed border-blue-500"></span>
                        <span>Transfer Hattı</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Transfers;
