import React, { useState } from 'react';
import { Search, SlidersHorizontal, Star, Heart, Plus } from 'lucide-react';
import { clsx } from 'clsx';
import { useCart } from '../../context/CartContext';
import { useFavorites } from '../../context/FavoritesContext';

export default function ShopScreen({ products }) {
    const { addToCart, cartItems } = useCart();
    const { toggleFavorite, isFavorite } = useFavorites();

    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('Hepsi');
    const [activeSort, setActiveSort] = useState('varsayilan'); // varsayilan, artan, azalan, yeni, mevsim
    const [isSortOpen, setIsSortOpen] = useState(false);

    const categories = ['Hepsi', 'Tişört', 'Ayakkabı', 'Aksesuar', 'Dış Giyim', 'Pantolon'];

    const getQuantityInCart = (id) => {
        const item = cartItems.find(i => i.id === id);
        return item ? item.quantity : 0;
    };

    // Filter and Sort Logic
    const filteredProducts = products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'Hepsi' || product.category === selectedCategory;
        return matchesSearch && matchesCategory;
    }).sort((a, b) => {
        if (activeSort === 'artan') return parseFloat(a.price) - parseFloat(b.price);
        if (activeSort === 'azalan') return parseFloat(b.price) - parseFloat(a.price);
        if (activeSort === 'yeni') return b.id - a.id; // Assuming higher ID is newer
        // 'mevsim' logic would go here if we had seasonal data, for now keep default
        return 0;
    });

    return (
        <div className="p-6 pt-12 pb-24 min-h-screen bg-white relative">
            {/* Header */}
            <h1 className="text-3xl font-bold text-gray-900 mb-6 font-display">Mağaza</h1>

            {/* Search Bar */}
            <div className="flex gap-3 mb-6">
                <div className="flex-1 bg-gray-50 rounded-2xl flex items-center px-4 py-3 border border-gray-100">
                    <Search size={20} className="text-gray-400 mr-3" />
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Ne aramıştınız?"
                        className="bg-transparent w-full focus:outline-none text-gray-900 font-medium placeholder:text-gray-400"
                    />
                </div>
                <button
                    onClick={() => setIsSortOpen(true)}
                    className="bg-gray-900 text-white w-14 rounded-2xl flex items-center justify-center hover:bg-black transition-colors"
                >
                    <SlidersHorizontal size={20} />
                </button>
            </div>

            {/* Horizontal Filter Pills */}
            <div className="flex overflow-x-auto gap-2 pb-6 -mx-6 px-6 scrollbar-hide mb-2">
                {categories.map((cat) => (
                    <button
                        key={cat}
                        onClick={() => setSelectedCategory(cat)}
                        className={clsx(
                            "px-5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-all",
                            selectedCategory === cat
                                ? "bg-gray-900 text-white shadow-lg shadow-gray-200"
                                : "bg-gray-50 text-gray-500 hover:bg-gray-100"
                        )}
                    >
                        {cat}
                    </button>
                ))}
            </div>

            {/* Products Grid */}
            <div className="grid grid-cols-2 gap-4">
                {filteredProducts.map((product) => {
                    const isFav = isFavorite(product.id);
                    const qty = getQuantityInCart(product.id);

                    return (
                        <div key={product.id} className="group relative">
                            <div className="bg-gray-50 rounded-3xl p-4 mb-3 relative overflow-hidden transition-all duration-300 group-hover:shadow-lg group-hover:-translate-y-1">

                                {/* Product Actions */}
                                <div className="absolute top-3 right-3 flex flex-col gap-2 z-10 translate-x-10 group-hover:translate-x-0 transition-transform duration-300">
                                    <button
                                        onClick={() => toggleFavorite(product)}
                                        className="w-8 h-8 bg-white/90 backdrop-blur rounded-full flex items-center justify-center shadow-sm text-gray-900 hover:text-red-500 transition-colors"
                                    >
                                        <Heart size={16} fill={isFav ? "currentColor" : "none"} className={isFav ? "text-red-500" : ""} />
                                    </button>
                                    <button
                                        onClick={() => addToCart(product)}
                                        className="w-8 h-8 bg-gray-900 rounded-full flex items-center justify-center shadow-sm text-white hover:bg-black transition-colors relative"
                                    >
                                        <Plus size={16} />
                                        {qty > 0 && (
                                            <span className="absolute -top-1 -right-1 w-4 h-4 bg-indigo-600 rounded-full text-[10px] flex items-center justify-center border border-white">
                                                {qty}
                                            </span>
                                        )}
                                    </button>
                                </div>

                                <div className="aspect-[4/5] flex items-center justify-center mb-2">
                                    <img
                                        src={product.image}
                                        alt={product.name}
                                        className="w-3/4 h-3/4 object-contain mix-blend-normal group-hover:scale-110 transition-transform duration-500"
                                    />
                                </div>
                            </div>

                            <div className="space-y-1 px-1">
                                <div className="flex justify-between items-start">
                                    <h3 className="font-bold text-gray-900 text-sm leading-tight flex-1 mr-2">{product.name}</h3>
                                    <div className="flex items-center gap-1 text-orange-500 shrink-0">
                                        <Star size={12} fill="currentColor" />
                                        <span className="text-xs font-bold">4.8</span>
                                    </div>
                                </div>
                                <p className="text-gray-500 text-xs">{product.category || 'Giyim'}</p>
                                <p className="font-bold text-indigo-600 text-base mt-1">{product.price}</p>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Sort Bottom Sheet */}
            {isSortOpen && (
                <>
                    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40" onClick={() => setIsSortOpen(false)} />
                    <div className="fixed bottom-0 left-0 w-full bg-white rounded-t-3xl p-6 z-50 animate-in slide-in-from-bottom duration-300">
                        <div className="w-12 h-1.5 bg-gray-200 rounded-full mx-auto mb-6" />
                        <h3 className="text-xl font-bold text-gray-900 mb-4">Sıralama Seçenekleri</h3>
                        <div className="space-y-2">
                            {[
                                { id: 'varsayilan', label: 'Varsayılan Sıralama' },
                                { id: 'mevsim', label: 'Mevsimine Göre Kombinler 🍂', highlight: true },
                                { id: 'yeni', label: 'En Yeniler' },
                                { id: 'artan', label: 'Fiyata Göre (Artan)' },
                                { id: 'azalan', label: 'Fiyata Göre (Azalan)' },
                            ].map((opt) => (
                                <button
                                    key={opt.id}
                                    onClick={() => {
                                        setActiveSort(opt.id);
                                        setIsSortOpen(false);
                                    }}
                                    className={clsx(
                                        "w-full p-4 rounded-xl text-left font-semibold transition-colors flex justify-between items-center",
                                        activeSort === opt.id
                                            ? "bg-indigo-50 text-indigo-700"
                                            : "bg-gray-50 text-gray-700 hover:bg-gray-100",
                                        opt.highlight && "border border-orange-200 bg-orange-50 text-orange-700"
                                    )}
                                >
                                    {opt.label}
                                    {activeSort === opt.id && <div className="w-2 h-2 rounded-full bg-indigo-600" />}
                                </button>
                            ))}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
