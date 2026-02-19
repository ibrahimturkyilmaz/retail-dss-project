import { motion } from 'framer-motion';
import { Heart, ShoppingBag } from 'lucide-react';
import { useFavorites } from '../../context/FavoritesContext';
import { useCart } from '../../context/CartContext';

export default function FavoritesScreen() {
    const { favorites, toggleFavorite } = useFavorites();
    const { addToCart } = useCart();

    if (favorites.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[70vh] p-6 text-center">
                <div className="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-4">
                    <Heart size={32} className="text-gray-300" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Favorileriniz Boş</h3>
                <p className="text-gray-500 max-w-xs">
                    Beğendiğiniz ürünleri buraya ekleyerek daha sonra kolayca bulabilirsiniz.
                </p>
            </div>
        );
    }

    return (
        <div className="p-6 pt-12 pb-24 min-h-screen bg-gray-50/50">
            <h1 className="text-2xl font-bold text-gray-900 mb-6 px-1">Favorilerim ({favorites.length})</h1>

            <div className="grid grid-cols-2 gap-4">
                {favorites.map((product) => (
                    <motion.div
                        layout
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        key={product.id}
                        className="bg-white rounded-2xl p-3 shadow-sm border border-gray-100 relative group"
                    >
                        {/* Remove Button */}
                        <button
                            onClick={() => toggleFavorite(product)}
                            className="absolute top-3 right-3 w-8 h-8 bg-white rounded-full shadow-sm flex items-center justify-center text-red-500 z-10"
                        >
                            <Heart size={16} fill="currentColor" />
                        </button>

                        <div className="aspect-square bg-gray-50 rounded-xl mb-3 flex items-center justify-center relative overflow-hidden">
                            <img
                                src="https://cdn-icons-png.flaticon.com/512/2829/2829824.png" // Placeholder, in real app use product.image
                                className="w-20 h-20 object-contain mix-blend-multiply group-hover:scale-110 transition-transform duration-300"
                                alt={product.name}
                            />
                        </div>

                        <div className="space-y-1">
                            <h3 className="font-bold text-gray-800 text-sm truncate">{product.name}</h3>
                            <p className="text-xs text-gray-500">{product.category || 'Giyim'}</p>

                            <div className="flex items-center justify-between pt-2">
                                <span className="font-bold text-indigo-600 text-sm">{product.price}</span>
                                <button
                                    onClick={() => addToCart(product)}
                                    className="w-8 h-8 bg-gray-900 rounded-full flex items-center justify-center text-white active:scale-95 transition-transform"
                                >
                                    <ShoppingBag size={14} />
                                </button>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
