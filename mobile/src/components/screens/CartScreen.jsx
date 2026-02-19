import { motion, AnimatePresence } from 'framer-motion';
import { Minus, Plus, Trash2, ArrowRight } from 'lucide-react';
import { useCart } from '../../context/CartContext';

export default function CartScreen() {
    const { cartItems, updateQuantity, removeFromCart, cartTotal } = useCart();

    if (cartItems.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[70vh] p-6 text-center">
                <div className="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-4">
                    <img src="https://cdn-icons-png.flaticon.com/512/11329/11329060.png" width="40" className="opacity-40" alt="Empty Cart" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Sepetiniz Boş</h3>
                <p className="text-gray-500 max-w-xs">
                    Henüz sepetinize ürün eklememişsiniz. Alışverişe başlayın!
                </p>
            </div>
        );
    }

    return (
        <div className="p-6 pt-12 pb-32 min-h-screen bg-gray-50/50 flex flex-col">
            <h1 className="text-2xl font-bold text-gray-900 mb-6 px-1">Sepetim ({cartItems.length})</h1>

            <div className="flex-1 space-y-4">
                <AnimatePresence>
                    {cartItems.map((item) => (
                        <motion.div
                            key={item.id}
                            layout
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, x: -100 }}
                            className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex gap-4"
                        >
                            <div className="w-20 h-20 bg-gray-50 rounded-xl flex items-center justify-center shrink-0">
                                <img
                                    src="https://cdn-icons-png.flaticon.com/512/2829/2829824.png"
                                    className="w-12 h-12 object-contain mix-blend-multiply"
                                    alt={item.name}
                                />
                            </div>

                            <div className="flex-1 flex flex-col justify-between">
                                <div>
                                    <div className="flex justify-between items-start">
                                        <h3 className="font-bold text-gray-800 text-sm line-clamp-1">{item.name}</h3>
                                        <button
                                            onClick={() => removeFromCart(item.id)}
                                            className="text-gray-400 hover:text-red-500 transition-colors p-1"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                    <p className="text-xs text-gray-500">{item.category || 'Giyim'}</p>
                                </div>

                                <div className="flex justify-between items-end mt-2">
                                    <span className="font-bold text-indigo-600">{item.price}</span>

                                    <div className="flex items-center gap-3 bg-gray-50 rounded-lg px-2 py-1">
                                        <button
                                            onClick={() => updateQuantity(item.id, -1)}
                                            className="w-6 h-6 flex items-center justify-center bg-white rounded-md shadow-sm text-gray-600 hover:text-indigo-600"
                                        >
                                            <Minus size={12} />
                                        </button>
                                        <span className="text-sm font-bold w-4 text-center">{item.quantity}</span>
                                        <button
                                            onClick={() => updateQuantity(item.id, 1)}
                                            className="w-6 h-6 flex items-center justify-center bg-white rounded-md shadow-sm text-gray-600 hover:text-indigo-600"
                                        >
                                            <Plus size={12} />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            {/* Bottom Summary Panel */}
            <div className="fixed bottom-20 left-0 w-full px-6 bg-gradient-to-t from-white via-white to-transparent pt-10 pb-4 z-40">
                <div className="max-w-md mx-auto bg-white rounded-3xl shadow-[0_-4px_20px_rgba(0,0,0,0.1)] p-5 border border-gray-100">
                    <div className="flex justify-between items-center mb-4">
                        <span className="text-gray-500 text-sm font-medium">Toplam Tutar</span>
                        <span className="text-2xl font-bold text-gray-900">{cartTotal.toFixed(2)} ₺</span>
                    </div>
                    <button className="w-full bg-gray-900 text-white py-4 rounded-xl font-bold flex items-center justify-between px-6 hover:bg-black transition-colors">
                        <span>Satın Al</span>
                        <div className="bg-white/20 p-2 rounded-full">
                            <ArrowRight size={20} />
                        </div>
                    </button>
                </div>
            </div>
        </div>
    );
}
