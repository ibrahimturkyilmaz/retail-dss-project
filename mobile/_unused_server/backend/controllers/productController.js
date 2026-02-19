const { sql } = require('../config/db');
const NodeCache = require('node-cache');
const productCache = new NodeCache({ stdTTL: 60 }); // 60 Saniye önbellekleme

exports.getProducts = async (req, res) => {
    try {
        // 1. Önce Cache kontrol et
        const cachedProducts = productCache.get("all_products");
        if (cachedProducts) {
            console.log("Serving Products from Cache ⚡");
            return res.json(cachedProducts);
        }

        const pool = await sql.connect();

        // 2. Cache yoksa veritabanından çek (Inventory ID eklendi)
        const query = `
            SELECT 
                p.product_id,
                p.product_name,
                p.category,
                p.price,
                i.inventory_id,
                i.store_id,
                s.store_name,
                i.stock_quantity
            FROM Products p
            LEFT JOIN Inventory i ON p.product_id = i.product_id
            LEFT JOIN Stores s ON i.store_id = s.store_id
            WHERE i.stock_quantity > 0
        `;

        const result = await pool.request().query(query);

        const products = result.recordset.map(item => ({
            id: item.product_id,
            inventoryId: item.inventory_id, // Critical for Cart
            name: item.product_name,
            category: item.category,
            price: item.price + " ₺",
            store: item.store_name,
            image: "https://cdn-icons-png.flaticon.com/512/2829/2829824.png"
        }));

        // 3. Sonucu Cache'e kaydet
        productCache.set("all_products", products);
        console.log("Serving Products from SQL (and caching) 💾");

        res.json(products);

    } catch (error) {
        console.error('Product Fetch Error:', error);
        res.status(500).json({ message: 'Veriler çekilemedi.' });
    }
};
