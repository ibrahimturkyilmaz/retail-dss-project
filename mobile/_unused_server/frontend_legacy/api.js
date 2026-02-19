import axios from 'axios';

// Temel API Adresi (Base URL) yapılandırması
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const api = {
    // Mağazalar - Backend'de henüz bir mağaza servisi bulunmadığı için geçici (mock) veri döndürülüyor.
    // Gelecekte burası gerçek bir API endpoint'ine bağlanabilir.
    fetchStores: async () => {
        // Mock Stores
        return new Promise(resolve => setTimeout(() => resolve([
            { id: 'store_001', name: 'Nişantaşı Flagship', lat: 41.0522, lng: 28.9959 }
        ]), 500));
    },

    // Ürünler - Backend'deki ürünler servisine gerçek bir API çağrısı yapar.
    fetchProducts: async () => {
        try {
            const response = await apiClient.get('/products');
            return response.data;
        } catch (error) {
            console.error("API Error (Products):", error);
            throw error;
        }
    },

    // Giriş (Login) - Gerçek API Çağrısı
    login: async (email, password) => {
        try {
            const response = await apiClient.post('/auth/login', { email, password });
            return response.data.user;
        } catch (error) {
            console.error("API Error (Login):", error);
            throw error;
        }
    },

    // Kullanıcı Profili - Giriş sonrası elimizde veri olduğu için şu an kullanılmıyor (Legacy)
    fetchUserProfile: async () => {
        return null;
    }
};
