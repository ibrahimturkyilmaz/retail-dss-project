import React, { useState } from 'react';
import { Search, SlidersHorizontal, Star, Heart, Plus, BadgeCheck } from 'lucide-react';
import { clsx } from 'clsx';
import { useCart } from '../../context/CartContext';
import { useFavorites } from '../../context/FavoritesContext';
import { motion, AnimatePresence } from 'framer-motion';

export default function ShopScreen({ products }) {
    const { addToCart, cartItems } = useCart();
    const { toggleFavorite, isFavorite } = useFavorites();

    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('Hepsi');
    const [activeSort, setActiveSort] = useState('varsayilan');
    const [isSortOpen, setIsSortOpen] = useState(false);

    const categories = ['Hepsi', 'Tişört', 'Ayakkabı', 'Aksesuar', 'Dış Giyim', 'Pantolon'];

    const getQuantityInCart = (id) => {
        const item = cartItems.find(i => i.id === id);
        return item ? item.quantity : 0;
    };

    const filteredProducts = products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'Hepsi' || product.category === selectedCategory;
        return matchesSearch && matchesCategory;
    }).sort((a, b) => {
        if (activeSort === 'artan') return parseFloat(a.price) - parseFloat(b.price);
        if (activeSort === 'azalan') return parseFloat(b.price) - parseFloat(a.price);
        if (activeSort === 'yeni') return b.id - a.id;
        return 0;
    });

    return (
        <div className="p-6 pt-12 pb-24 min-h-screen bg-slate-50 relative">
            {/* Header */}
            <h1 className="text-3xl font-extrabold text-slate-900 mb-6 font-heading tracking-tight">Mağaza</h1>

            {/* Sticky Search & Filter */}
            <div className="sticky top-2 z-30 bg-slate-50/95 backdrop-blur-sm py-2 -mx-6 px-6 mb-4">
                <div className="flex gap-3">
                    <div className="flex-1 bg-white rounded-2xl flex items-center px-4 py-3.5 border border-slate-200 shadow-sm focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-100 transition-all">
                        <Search size={20} className="text-slate-400 mr-3" />
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Marka, ürün veya kategori ara..."
                            className="bg-transparent w-full focus:outline-none text-slate-900 font-medium placeholder:text-slate-400"
                        />
                    </div>
                    <button
                        onClick={() => setIsSortOpen(true)}
                        className="bg-slate-900 text-white w-14 rounded-2xl flex items-center justify-center hover:bg-indigo-600 transition-colors shadow-lg shadow-slate-200"
                    >
                        <SlidersHorizontal size={20} />
                    </button>
                </div>

                {/* Categories */}
                <div className="flex overflow-x-auto gap-2 py-4 hide-scrollbar">
                    {categories.map((cat) => (
                        <button
                            key={cat}
                            onClick={() => setSelectedCategory(cat)}
                            className={clsx(
                                "px-5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-all border",
                                selectedCategory === cat
                                    ? "bg-slate-900 text-white border-slate-900 shadow-md transform scale-105"
                                    : "bg-white text-slate-500 border-slate-200 hover:border-slate-300 hover:text-slate-700"
                            )}
                        >
                            {cat}
                        </button>
                    ))}
                </div>
            </div>

            {/* Products Grid */}
            <div className="grid grid-cols-2 gap-4">
                {filteredProducts.map((product) => {
                    const isFav = isFavorite(product.id);
                    const qty = getQuantityInCart(product.id);

                    return (
                        <motion.div
                            layout
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            key={product.id} className="card group relative overflow-visible"
                        >
                            <div className="p-3 pb-0">
                                <div className="bg-slate-50 rounded-2xl p-4 mb-3 relative overflow-hidden transition-all duration-300 group-hover:bg-slate-100 aspect-[3/4] flex items-center justify-center">
                                    <div className="absolute top-3 right-3 flex flex-col gap-2 z-10">
                                        <button
                                            onClick={(e) => { e.stopPropagation(); toggleFavorite(product); }}
                                            className="w-8 h-8 bg-white/80 backdrop-blur rounded-full flex items-center justify-center shadow-sm text-slate-400 hover:text-red-500 hover:bg-white transition-all scale-0 group-hover:scale-100"
                                        >
                                            <Heart size={16} fill={isFav ? "currentColor" : "none"} className={isFav ? "text-red-500" : ""} />
                                        </button>
                                    </div>

                                    <img
                                        src={product.image}
                                        alt={product.name}
                                        className="w-full h-full object-contain mix-blend-multiply group-hover:scale-105 transition-transform duration-500"
                                    />

                                    {/* Quick Add Button on Image */}
                                    <button
                                        onClick={(e) => { e.stopPropagation(); addToCart(product); }}
                                        className="absolute bottom-3 right-3 w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center shadow-lg text-white hover:bg-indigo-600 hover:scale-110 active:scale-95 transition-all z-20"
                                    >
                                        <Plus size={20} />
                                        {qty > 0 && (
                                            <span className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full text-[10px] font-bold flex items-center justify-center border-2 border-white">
                                                {qty}
                                            </span>
                                        )}
                                    </button>
                                </div>
                            </div>

                            <div className="px-4 pb-4 space-y-1">
                                <div className="flex justify-between items-start">
                                    <h3 className="font-bold text-slate-900 text-sm leading-tight line-clamp-2">{product.name}</h3>
                                </div>
                                <div className="flex items-center gap-1.5 pt-1">
                                    <div className="flex gap-0.5 text-yellow-400">
                                        <Star size={12} fill="currentColor" />
                                    </div>
                                    <span className="text-xs font-semibold text-slate-400">4.8 (120+)</span>
                                </div>
                                <p className="font-extrabold text-indigo-600 text-lg pt-1">{product.price}</p>
                            </div>
                        </motion.div>
                    );
                })}
            </div>

            {/* Sort Bottom Sheet - Improved Design */}
            <AnimatePresence>
                {isSortOpen && (
                    <>
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40"
                            onClick={() => setIsSortOpen(false)}
                        />
                        <motion.div
                            initial={{ y: '100%' }}
                            animate={{ y: 0 }}
                            exit={{ y: '100%' }}
                            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
                            className="fixed bottom-0 left-0 w-full bg-white rounded-t-[2rem] p-6 z-50 shadow-2xl"
                        >
                            <div className="w-16 h-1.5 bg-slate-200 rounded-full mx-auto mb-8" />

                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-2xl font-bold text-slate-900 font-heading">Sıralama</h3>
                                <button onClick={() => setIsSortOpen(false)} className="text-slate-400 hover:text-slate-600 font-medium">Bitti</button>
                            </div>

                            <div className="space-y-3">
                                {[
                                    { id: 'varsayilan', label: 'Önerilen Sıralama', icon: <BadgeCheck size={18} /> },
                                    { id: 'mevsim', label: 'Bu Sezonun Trendleri 🔥', highlight: true },
                                    { id: 'yeni', label: 'En Yeniler' },
                                    { id: 'artan', label: 'Fiyat: Düşükten Yükseğe' },
                                    { id: 'azalan', label: 'Fiyat: Yüksekten Düşüğe' },
                                ].map((opt) => (
                                    <button
                                        key={opt.id}
                                        onClick={() => {
                                            setActiveSort(opt.id);
                                            setIsSortOpen(false);
                                        }}
                                        className={clsx(
                                            "w-full p-4 rounded-2xl text-left font-bold transition-all flex justify-between items-center border",
                                            activeSort === opt.id
                                                ? "bg-indigo-50 text-indigo-700 border-indigo-200 shadow-sm"
                                                : "bg-white text-slate-600 border-slate-100 hover:bg-slate-50",
                                            opt.highlight && activeSort !== opt.id && "bg-orange-50 text-orange-700 border-orange-100"
                                        )}
                                    >
                                        <div className="flex items-center gap-3">
                                            {opt.icon}
                                            {opt.label}
                                        </div>
                                        {activeSort === opt.id && <div className="w-2.5 h-2.5 rounded-full bg-indigo-600 shadow-[0_0_10px_rgba(79,70,229,0.5)]" />}
                                    </button>
                                ))}
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </div>
    );
}
