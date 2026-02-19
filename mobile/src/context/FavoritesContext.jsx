import { createContext, useContext, useState, useEffect } from 'react';

const FavoritesContext = createContext();

export function FavoritesProvider({ children }) {
    // Initialize favorites from LocalStorage
    const [favorites, setFavorites] = useState(() => {
        try {
            const storedFavs = localStorage.getItem('favorites');
            return storedFavs ? JSON.parse(storedFavs) : [];
        } catch (error) {
            console.error("Failed to parse favorites from local storage", error);
            return [];
        }
    });

    // Save to LocalStorage whenever favorites changes
    useEffect(() => {
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }, [favorites]);

    const toggleFavorite = (product) => {
        setFavorites(prev => {
            const isFav = prev.some(item => item.id === product.id);
            if (isFav) {
                return prev.filter(item => item.id !== product.id);
            }
            return [...prev, product];
        });
    };

    const isFavorite = (productId) => {
        return favorites.some(item => item.id === productId);
    };

    return (
        <FavoritesContext.Provider value={{ favorites, toggleFavorite, isFavorite }}>
            {children}
        </FavoritesContext.Provider>
    );
}

export const useFavorites = () => useContext(FavoritesContext);
