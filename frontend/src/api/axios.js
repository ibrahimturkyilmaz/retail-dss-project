import axios from 'axios';

const axiosClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000', // Backend URL
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor
axiosClient.interceptors.request.use(
    (config) => {
        // Gelecekte token ekleme vs. burada yapılabilir
        // console.log(`[API] İstek gönderiliyor: ${config.url}`);
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response Interceptor
axiosClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // Merkezi hata yönetimi
        if (error.response) {
            console.error('[API Hatası]', error.response.status, error.response.data);
        } else {
            console.error('[Network Hatası]', error.message);
        }
        return Promise.reject(error);
    }
);

export default axiosClient;
