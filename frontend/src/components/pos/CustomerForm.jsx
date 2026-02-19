import React, { useState, useEffect } from 'react';
import { UserPlusIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';

const CustomerForm = ({ onConfirm, onCancel, totalAmount }) => {
    // Search Mode
    const [searchTerm, setSearchTerm] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [loading, setLoading] = useState(false);

    // Selected Customer
    const [selectedCustomer, setSelectedCustomer] = useState(null);
    const [usePoints, setUsePoints] = useState(false);

    // Create Mode
    const [isCreating, setIsCreating] = useState(false);
    const [newCustomer, setNewCustomer] = useState({ name: "", phone: "", email: "", city: "" });

    // --- Search Logic ---
    useEffect(() => {
        const delayDebounceFn = setTimeout(async () => {
            if (searchTerm.length > 2) {
                setLoading(true);
                try {
                    const res = await fetch(`http://localhost:8000/api/customers/search?q=${searchTerm}`);
                    if (res.ok) {
                        const data = await res.json();
                        setSearchResults(data);
                    }
                } catch (err) {
                    console.error("Search failed", err);
                } finally {
                    setLoading(false);
                }
            } else {
                setSearchResults([]);
            }
        }, 500);

        return () => clearTimeout(delayDebounceFn);
    }, [searchTerm]);

    // --- Actions ---
    const handleSelect = (cust) => {
        setSelectedCustomer(cust);
        setSearchTerm("");
        setSearchResults([]);
        setUsePoints(false); // Reset
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch(`http://localhost:8000/api/customers`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newCustomer)
            });

            if (res.ok) {
                const created = await res.json();
                setSelectedCustomer(created);
                setIsCreating(false);
            } else {
                const err = await res.json();
                alert(`Hata: ${err.detail}`);
            }
        } catch (err) {
            alert("Bağlantı hatası");
        }
    };

    const handleConfirm = () => {
        if (!selectedCustomer) return alert("Lütfen bir müşteri seçin veya oluşturun.");
        // Return customer and point usage choice
        onConfirm({ ...selectedCustomer, usePoints });
    };

    // Calculate Payment Details
    const pointsAvailable = selectedCustomer?.points_balance || 0;
    const pointsToUse = usePoints ? Math.min(pointsAvailable, totalAmount) : 0;
    const remainingToPay = totalAmount - pointsToUse;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl p-6 w-full max-w-lg shadow-2xl overflow-hidden">
                <h2 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-2">
                    {isCreating ? "Yeni Müşteri Oluştur" : "Müşteri Seçimi & Ödeme"}
                </h2>

                {!isCreating ? (
                    <>
                        {/* Selected Customer View */}
                        {selectedCustomer ? (
                            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 mb-6 relative">
                                <button
                                    onClick={() => setSelectedCustomer(null)}
                                    className="absolute top-2 right-2 text-gray-400 hover:text-red-500"
                                >
                                    Değiştir
                                </button>
                                <h3 className="font-bold text-lg text-emerald-800">{selectedCustomer.name}</h3>
                                <p className="text-sm text-gray-600">{selectedCustomer.phone} | {selectedCustomer.email}</p>
                                <div className="mt-3 flex gap-4">
                                    <div className="bg-white p-2 rounded-lg shadow-sm border border-emerald-100 flex-1 text-center">
                                        <div className="text-xs text-gray-500 uppercase">Puan Bakiyesi</div>
                                        <div className="font-bold text-xl text-emerald-600">{selectedCustomer.points_balance.toFixed(0)} P</div>
                                    </div>
                                    <div className="bg-white p-2 rounded-lg shadow-sm border border-emerald-100 flex-1 text-center">
                                        <div className="text-xs text-gray-500 uppercase">Alışveriş Sayısı</div>
                                        <div className="font-bold text-xl text-emerald-600">{selectedCustomer.total_shopping_count}</div>
                                    </div>
                                </div>

                                {/* Point Usage Section */}
                                {pointsAvailable > 0 && (
                                    <div className="mt-4 pt-3 border-t border-emerald-100">
                                        <label className="flex items-center space-x-3 cursor-pointer">
                                            <input
                                                type="checkbox"
                                                className="w-5 h-5 text-emerald-600 rounded focus:ring-emerald-500"
                                                checked={usePoints}
                                                onChange={(e) => setUsePoints(e.target.checked)}
                                            />
                                            <span className="text-gray-700 font-medium">Puan Kullan ({pointsAvailable.toFixed(0)} TL)</span>
                                        </label>
                                        {usePoints && (
                                            <div className="mt-2 text-sm text-emerald-700 bg-emerald-100 p-2 rounded">
                                                -{pointsToUse.toFixed(2)} TL Puanla ödenecek.
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        ) : (
                            /* Search View */
                            <div className="mb-6 relative">
                                <div className="relative">
                                    <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-3.5 text-gray-400" />
                                    <input
                                        type="text"
                                        className="w-full border p-3 pl-10 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none"
                                        placeholder="İsim veya Telefon ile ara..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                        autoFocus
                                    />
                                    {loading && <div className="absolute right-3 top-3.5 animate-spin h-5 w-5 border-2 border-emerald-500 rounded-full border-t-transparent"></div>}
                                </div>

                                {searchResults.length > 0 && (
                                    <ul className="absolute z-10 w-full bg-white border border-gray-100 rounded-xl shadow-xl mt-2 max-h-60 overflow-y-auto">
                                        {searchResults.map((c) => (
                                            <li
                                                key={c.id}
                                                className="p-3 hover:bg-emerald-50 cursor-pointer border-b last:border-0 flex justify-between items-center"
                                                onClick={() => handleSelect(c)}
                                            >
                                                <div>
                                                    <div className="font-bold text-gray-700">{c.name}</div>
                                                    <div className="text-xs text-gray-500">{c.phone}</div>
                                                </div>
                                                <div className="text-emerald-600 font-bold text-sm bg-emerald-50 px-2 py-1 rounded">
                                                    {c.points_balance} P
                                                </div>
                                            </li>
                                        ))}
                                    </ul>
                                )}

                                <div className="mt-4 text-center">
                                    <span className="text-gray-500 text-sm">Müşteri bulunamadı mı?</span>
                                    <button
                                        onClick={() => setIsCreating(true)}
                                        className="ml-2 text-emerald-600 font-bold hover:underline flex items-center justify-center gap-1 mx-auto mt-1"
                                    >
                                        <UserPlusIcon className="w-4 h-4" /> Yeni Oluştur
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* Summary */}
                        {selectedCustomer && (
                            <div className="mb-4 bg-gray-50 p-3 rounded-xl flex justify-between items-center">
                                <span className="text-gray-500">Ödenecek Tutar:</span>
                                <span className="text-xl font-bold text-gray-800">{remainingToPay.toFixed(2)} TL</span>
                            </div>
                        )}

                        <div className="flex gap-3 mt-4">
                            <button
                                onClick={onCancel}
                                className="flex-1 bg-gray-100 text-gray-700 font-bold py-3 rounded-xl hover:bg-gray-200"
                            >
                                İptal
                            </button>
                            <button
                                onClick={handleConfirm}
                                disabled={!selectedCustomer}
                                className="flex-1 bg-emerald-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl hover:bg-emerald-700 shadow-lg"
                            >
                                {remainingToPay === 0 ? "Tamamla" : "Ödemeye Geç"}
                            </button>
                        </div>
                    </>
                ) : (
                    /* Create View */
                    <form onSubmit={handleCreate}>
                        <div className="space-y-4 mb-6">
                            <div>
                                <label className="block text-sm text-gray-600 mb-1">Ad Soyad</label>
                                <input required className="w-full border p-2 rounded-lg" value={newCustomer.name} onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })} />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-600 mb-1">Telefon</label>
                                <input required className="w-full border p-2 rounded-lg" value={newCustomer.phone} onChange={e => setNewCustomer({ ...newCustomer, phone: e.target.value })} />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-600 mb-1">E-Posta (Fiş için)</label>
                                <input type="email" className="w-full border p-2 rounded-lg" value={newCustomer.email} onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })} />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-600 mb-1">Şehir</label>
                                <input className="w-full border p-2 rounded-lg" value={newCustomer.city} onChange={e => setNewCustomer({ ...newCustomer, city: e.target.value })} />
                            </div>
                        </div>
                        <div className="flex gap-3">
                            <button type="button" onClick={() => setIsCreating(false)} className="flex-1 bg-gray-100 py-3 rounded-xl font-bold">Geri</button>
                            <button type="submit" className="flex-1 bg-emerald-600 text-white py-3 rounded-xl font-bold shadow-lg">Kaydet</button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default CustomerForm;
