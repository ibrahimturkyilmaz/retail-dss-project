import React, { useState, useEffect, useRef } from 'react';
import { useTime } from '../context/TimeContext';
import CustomerForm from '../components/pos/CustomerForm';
import { QrCodeIcon, ShoppingCartIcon, ArrowPathIcon, TrashIcon, XMarkIcon } from '@heroicons/react/24/outline';

const QuantityModal = ({ product, onConfirm, onCancel }) => {
    const [qty, setQty] = useState(1);
    const inputRef = useRef(null);

    useEffect(() => {
        if (inputRef.current) inputRef.current.focus();
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (qty > 0) onConfirm(parseInt(qty));
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden">
                <div className="bg-emerald-600 p-4 text-white flex justify-between items-center">
                    <h3 className="font-bold text-lg">Miktar Girin</h3>
                    <button onClick={onCancel}><XMarkIcon className="w-6 h-6" /></button>
                </div>
                <div className="p-6">
                    <div className="mb-4 text-center">
                        <p className="text-gray-500 text-sm">Ürün:</p>
                        <p className="font-bold text-xl text-gray-800">{product.name}</p>
                        <p className="text-emerald-600 font-bold">{product.price} TL</p>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <input
                            ref={inputRef}
                            type="number"
                            min="1"
                            value={qty}
                            onChange={(e) => setQty(e.target.value)}
                            className="w-full text-center text-4xl font-bold border-2 border-emerald-500 rounded-xl p-4 mb-6 focus:outline-none focus:ring-4 focus:ring-emerald-200"
                        />
                        <button type="submit" className="w-full bg-emerald-600 text-white font-bold py-3 rounded-xl hover:bg-emerald-700 text-lg">
                            ONAYLA
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

const POS = () => {
    const { virtualTime } = useTime();

    // States
    const [mode, setMode] = useState('SALE'); // 'SALE' or 'RETURN'
    const [cart, setCart] = useState([]);
    const [isScanning, setIsScanning] = useState(false);
    const [showCustomerForm, setShowCustomerForm] = useState(false);
    const [returnReceiptNo, setReturnReceiptNo] = useState('');

    // Scanner
    const [showScanner, setShowScanner] = useState(false);

    // Scanned Product & Quantity Modal
    const [scannedProduct, setScannedProduct] = useState(null);
    const [showQtyModal, setShowQtyModal] = useState(false);

    // Derived
    const totalAmount = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    // --- Actions ---

    const handleScanClick = () => {
        // If mobile, open real scanner
        if (isMobile) {
            setShowScanner(true);
        } else {
            // Simulation for Desktop
            simulateScan();
        }
    };

    const handleBarcodeDetected = async (barcode) => {
        setShowScanner(false); // Close scanner on detection
        await processBarcode(barcode);
    };

    const processBarcode = async (barcode) => {
        setIsScanning(true);
        try {
            if (mode === 'SALE') {
                const res = await fetch(`http://localhost:8000/api/pos/products/scan/${barcode}`);
                if (res.ok) {
                    const product = await res.json();
                    setScannedProduct(product);
                    setShowQtyModal(true);
                } else {
                    alert("Barkod Bulunamadı / Ürün Yok");
                    // Re-open scanner if failed? Maybe not to annoy user.
                }
            } else {
                // Return Mode - Barcode might be receipt no or product?
                // Current logic expects Receipt No manual input or QR scan
                // If QR scan returns Receipt No:
                setReturnReceiptNo(barcode);
                alert(`Fiş No Okundu: ${barcode}`);
            }
        } catch (err) {
            console.error(err);
            alert("Hata oluştu");
        } finally {
            setIsScanning(false);
        }
    };

    const simulateScan = async () => {
        setIsScanning(true);
        setTimeout(async () => {
            try {
                if (mode === 'SALE') {
                    const randomId = Math.floor(Math.random() * 10) + 1;
                    const simulatedBarcode = (8690000000000 + randomId).toString();
                    await processBarcode(simulatedBarcode);
                } else {
                    const simulatedReceipt = prompt("Barkod Okundu! Fiş No Girin (Simülasyon):", "R-123456");
                    if (simulatedReceipt) setReturnReceiptNo(simulatedReceipt);
                    setIsScanning(false);
                }
            } catch (err) {
                setIsScanning(false);
            }
        }, 600);
    };

    const handleQuantityConfirm = (qty) => {
        if (scannedProduct) {
            addToCart(scannedProduct, qty);
            setScannedProduct(null);
            setShowQtyModal(false);
        }
    };

    const addToCart = (product, qty) => {
        setCart(prev => {
            const existing = prev.find(p => p.sku === product.sku);
            if (existing) {
                return prev.map(p => p.sku === product.sku ? { ...p, quantity: p.quantity + qty } : p);
            }
            return [...prev, { ...product, quantity: qty }];
        });
    };

    const removeFromCart = (sku) => {
        setCart(prev => prev.filter(p => p.sku !== sku));
    };

    const handleSaleComplete = async (customerData) => {
        try {
            // Logic for Points Payment
            let payments = [];
            let pointsUsed = 0;

            if (customerData.usePoints && customerData.points_balance > 0) {
                const pointsToUse = Math.min(customerData.points_balance, totalAmount);
                payments.push({ payment_method: "POINTS", amount: pointsToUse });
                pointsUsed = pointsToUse;

                const remaining = totalAmount - pointsToUse;
                if (remaining > 0) {
                    payments.push({ payment_method: "CREDIT_CARD", amount: remaining });
                }
            } else {
                payments.push({ payment_method: "CREDIT_CARD", amount: totalAmount });
            }

            const payload = {
                pos_device_id: "POS-MOBILE-01",
                receipt_no: `R-${Date.now()}`,
                transaction_type: "SALE",
                total_amount: totalAmount,
                currency: "TRY",
                items: cart.map(item => ({
                    product_sku: item.sku,
                    quantity: item.quantity,
                    unit_price: item.price
                })),
                payments: payments,
                created_at: virtualTime.toISOString()
            };

            // Call API with email and customer_id
            let url = `http://localhost:8000/api/pos/sales?`;
            if (customerData.email) url += `email=${customerData.email}&`;
            if (customerData.id) url += `customer_id=${customerData.id}`;
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                const data = await res.json();
                alert(`✅ Satış Başarılı!\nFiş No: ${data.receipt_no}\nMail Gönderildi: ${customerData.email}`);
                setCart([]);
                setShowCustomerForm(false);
            } else {
                const err = await res.json();
                alert(`❌ Hata: ${err.detail}`);
            }

        } catch (err) {
            console.error(err);
            alert("Bağlantı Hatası!");
        }
    };

    const handleReturnProcess = async () => {
        if (!returnReceiptNo) return alert("Lütfen fiş no okutun!");
        try {
            const res = await fetch(`http://localhost:8000/api/pos/returns?receipt_no=${returnReceiptNo}`, {
                method: 'POST'
            });
            if (res.ok) {
                alert("✅ İade İşlemi Başarılı! Stoklar güncellendi.");
                setReturnReceiptNo("");
            } else {
                const err = await res.json();
                alert(`❌ İade Başarısız: ${err.detail}`);
            }
        } catch (err) {
            alert("Bağlantı Hatası!");
        }
    };

    return (
        <div className={`min-h-screen flex flex-col ${mode === 'SALE' ? 'bg-emerald-50' : 'bg-rose-50'}`}>
            {/* --- Header --- */}
            <div className="bg-white shadow-sm p-4 flex justify-between items-center z-10 sticky top-0">
                <div className="flex bg-gray-100 rounded-lg p-1">
                    <button
                        onClick={() => setMode('SALE')}
                        className={`px-4 py-2 rounded-md font-bold text-sm transition-all ${mode === 'SALE' ? 'bg-emerald-500 text-white shadow-md' : 'text-gray-500'}`}
                    >
                        SATIŞ
                    </button>
                    <button
                        onClick={() => setMode('RETURN')}
                        className={`px-4 py-2 rounded-md font-bold text-sm transition-all ${mode === 'RETURN' ? 'bg-rose-500 text-white shadow-md' : 'text-gray-500'}`}
                    >
                        İADE
                    </button>
                </div>
                <div className="text-xs text-gray-400 font-mono">
                    POS-MOBILE-01
                </div>
            </div>

            {/* --- Main Content --- */}
            <div className="flex-1 p-4 pb-32 overflow-y-auto">
                {/* Scanner Area */}
                <div
                    onClick={handleScanClick}
                    className={`
                        w-full h-32 rounded-2xl border-4 border-dashed flex flex-col items-center justify-center cursor-pointer active:scale-95 transition-transform mb-4 shadow-sm
                        ${mode === 'SALE' ? 'border-emerald-300 bg-emerald-100/50 hover:bg-emerald-100' : 'border-rose-300 bg-rose-100/50 hover:bg-rose-100'}
                    `}
                >
                    <QrCodeIcon className={`w-10 h-10 mb-1 ${isScanning ? 'animate-pulse' : ''} ${mode === 'SALE' ? 'text-emerald-600' : 'text-rose-600'}`} />
                    <span className="font-bold text-base text-gray-700">
                        {isScanning ? 'Okunuyor...' : (mode === 'SALE' ? 'KAMERA İLE OKUT' : 'FİŞ OKUT')}
                    </span>
                </div>

                {/* List Area */}
                {mode === 'SALE' ? (
                    <div className="space-y-3">
                        {cart.length === 0 && (
                            <div className="text-center text-gray-400 py-10 flex flex-col items-center">
                                <ShoppingCartIcon className="w-12 h-12 mb-2 opacity-50" />
                                Sepet Boş
                            </div>
                        )}
                        {cart.map((item, idx) => (
                            <div key={idx} className="bg-white p-3 rounded-xl shadow-sm border border-gray-100 flex justify-between items-center animate-fadeIn">
                                <div className="flex-1">
                                    <h4 className="font-bold text-gray-800 text-sm">{item.name}</h4>
                                    <div className="text-xs text-gray-500">
                                        {item.sku}
                                    </div>
                                    <div className="text-xs text-emerald-600 font-bold mt-1">
                                        {item.quantity} x {item.price} TL
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <span className="font-bold text-gray-800">{(item.price * item.quantity).toFixed(2)}</span>
                                    <button onClick={() => removeFromCart(item.sku)} className="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100">
                                        <TrashIcon className="w-4 h-4" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-rose-100 text-center">
                        <h3 className="text-lg font-bold text-gray-700 mb-4">İade İşlemi</h3>
                        <input
                            type="text"
                            disabled
                            value={returnReceiptNo || "..."}
                            className="w-full bg-gray-100 p-4 rounded-lg text-center font-mono text-xl mb-4 border border-gray-300"
                        />
                        <p className="text-sm text-gray-500">
                            İade almak için müşterinin fişindeki QR kodu yukarıdaki alana dokunarak okutun.
                        </p>
                    </div>
                )}
            </div>

            {/* --- Bottom Bar --- */}
            <div className="fixed bottom-0 left-0 w-full bg-white p-4 shadow-[0_-4px_10px_-1px_rgba(0,0,0,0.1)] z-20 rounded-t-2xl">
                {mode === 'SALE' ? (
                    <div className="flex justify-between items-center gap-4">
                        <div className="flex-1">
                            <p className="text-xs text-gray-500 uppercase tracking-wide">Toplam</p>
                            <p className="text-2xl font-black text-emerald-600">{totalAmount.toFixed(2)} <span className="text-sm font-normal text-gray-400">TL</span></p>
                        </div>
                        <button
                            disabled={cart.length === 0}
                            onClick={() => setShowCustomerForm(true)}
                            className="bg-emerald-600 hover:bg-emerald-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-bold py-3 px-6 rounded-xl shadow-lg flex items-center gap-2 transform active:scale-95 transition-all"
                        >
                            ÖDE
                            <ShoppingCartIcon className="w-5 h-5" />
                        </button>
                    </div>
                ) : (
                    <button
                        disabled={!returnReceiptNo}
                        onClick={handleReturnProcess}
                        className="w-full bg-rose-600 hover:bg-rose-700 disabled:bg-gray-300 text-white font-bold py-4 rounded-xl shadow-lg flex justify-center items-center gap-2 transform active:scale-95 transition-all"
                    >
                        <ArrowPathIcon className="w-6 h-6" />
                        İADEYİ TAMAMLA
                    </button>
                )}
            </div>

            {/* --- Modals --- */}
            {showCustomerForm && (
                <CustomerForm
                    totalAmount={totalAmount}
                    onConfirm={handleSaleComplete}
                    onCancel={() => setShowCustomerForm(false)}
                />
            )}

            {showScanner && (
                <BarcodeScanner
                    onScanSuccess={handleBarcodeDetected}
                    onClose={() => setShowScanner(false)}
                />
            )}

            {showQtyModal && scannedProduct && (
                <QuantityModal
                    product={scannedProduct}
                    onConfirm={handleQuantityConfirm}
                    onCancel={() => setShowQtyModal(false)}
                />
            )}
        </div>
    );
};

export default POS;
