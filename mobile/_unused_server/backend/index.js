require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { connectDB } = require('./config/db');

const authRoutes = require('./routes/authRoutes');
const productRoutes = require('./routes/productRoutes');
const cartRoutes = require('./routes/cartRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

// Ara Yazılımlar (Middleware)
app.use(cors());
app.use(express.json());

// Rotalar (Routes)
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/cart', cartRoutes);

// Test Amaçlı Basit Rota
app.get('/', (req, res) => {
    res.json({ message: 'Retail App API is Running', status: 'OK' });
});

// Sunucuyu Başlat
const startServer = async () => {
    try {
        // Veritabanına Bağlan
        await connectDB();

        app.listen(PORT, () => {
            console.log(`Server running on http://localhost:${PORT}`);
        });
    } catch (error) {
        console.error('Failed to start server:', error);
    }
};

startServer();
