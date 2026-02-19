import { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext();

export function CartProvider({ children }) {
    // Initialize cart from LocalStorage
    const [cartItems, setCartItems] = useState(() => {
        try {
            const storedCart = localStorage.getItem('cart');
            return storedCart ? JSON.parse(storedCart) : [];
        } catch (error) {
            console.error("Failed to parse cart from local storage", error);
            return [];
        }
    });

    // Save to LocalStorage whenever cartItems changes
    useEffect(() => {
        localStorage.setItem('cart', JSON.stringify(cartItems));
    }, [cartItems]);

    const addToCart = (product) => {
        setCartItems(prev => {
            const existingItem = prev.find(item => item.id === product.id);
            if (existingItem) {
                // If item exists, increment quantity (or just ignore if simple unique items)
                // Assuming simple unique list or increment logic:
                return prev.map(item =>
                    item.id === product.id
                        ? { ...item, quantity: (item.quantity || 1) + 1 }
                        : item
                );
            }
            // Add new item with default quantity 1
            return [...prev, { ...product, quantity: 1 }];
        });
    };

    const removeFromCart = (cartId) => {
        setCartItems(prev => prev.filter(item => item.id !== cartId));
    };

    const updateQuantity = (cartId, delta) => {
        setCartItems(prev => prev.map(item => {
            if (item.id === cartId) {
                const newQuantity = Math.max(1, (item.quantity || 1) + delta);
                return { ...item, quantity: newQuantity };
            }
            return item;
        }));
    };

    const clearCart = () => {
        setCartItems([]);
    };

    const cartTotal = cartItems.reduce((total, item) => {
        const price = typeof item.price === 'string'
            ? parseFloat(item.price.replace(/[^0-9.-]+/g, ""))
            : item.price;
        return total + (price * (item.quantity || 1));
    }, 0);

    return (
        <CartContext.Provider value={{ cartItems, addToCart, removeFromCart, updateQuantity, clearCart, cartTotal }}>
            {children}
        </CartContext.Provider>
    );
}

export const useCart = () => useContext(CartContext);
