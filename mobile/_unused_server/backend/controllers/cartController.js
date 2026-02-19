const { sql } = require('../config/db');

// Sepeti Getir (Get Cart)
exports.getCart = async (req, res) => {
    const { customerId } = req.params; // /api/cart/:customerId
    try {
        const pool = await sql.connect();
        const query = `
            SELECT 
                c.cart_id,
                c.quantity,
                p.product_id,
                p.product_name,
                p.price,
                p.category,
                i.inventory_id
            FROM Carts c
            JOIN Inventory i ON c.inventory_id = i.inventory_id
            JOIN Products p ON i.product_id = p.product_id
            WHERE c.customer_id = @customerId
        `;

        const result = await pool.request()
            .input('customerId', sql.NVarChar, customerId)
            .query(query);

        const cartItems = result.recordset.map(item => ({
            id: item.cart_id, // Frontend uses this internal ID for deletion logic usually, or product ID
            productId: item.product_id,
            inventoryId: item.inventory_id,
            name: item.product_name,
            price: item.price + " ₺",
            quantity: item.quantity,
            category: item.category
        }));

        res.json(cartItems);
    } catch (error) {
        console.error('Get Cart Error:', error);
        res.status(500).json({ message: 'Sepet getirilemedi.' });
    }
};

// Sepete Ekle (Add to Cart)
exports.addToCart = async (req, res) => {
    const { customerId, inventoryId, quantity } = req.body;

    try {
        const pool = await sql.connect();

        // Check if item already exists in cart for this user
        const checkQuery = `SELECT cart_id, quantity FROM Carts WHERE customer_id = @customerId AND inventory_id = @inventoryId`;
        const checkResult = await pool.request()
            .input('customerId', sql.NVarChar, customerId)
            .input('inventoryId', sql.NVarChar, inventoryId)
            .query(checkQuery);

        if (checkResult.recordset.length > 0) {
            // Update quantity
            const existingItem = checkResult.recordset[0];
            const newQty = existingItem.quantity + (quantity || 1);

            await pool.request()
                .input('qty', sql.Int, newQty)
                .input('id', sql.Int, existingItem.cart_id)
                .query(`UPDATE Carts SET quantity = @qty WHERE cart_id = @id`);

            res.json({ message: 'Sepet güncellendi', cartId: existingItem.cart_id });
        } else {
            // Insert new
            await pool.request()
                .input('customerId', sql.NVarChar, customerId)
                .input('inventoryId', sql.NVarChar, inventoryId)
                .input('qty', sql.Int, quantity || 1)
                .query(`INSERT INTO Carts (customer_id, inventory_id, quantity) VALUES (@customerId, @inventoryId, @qty)`);

            res.status(201).json({ message: 'Ürün sepete eklendi' });
        }

    } catch (error) {
        console.error('Add Cart Error:', error);
        res.status(500).json({ message: 'Sepete eklenemedi.' });
    }
};

// Sepetten Sil (Remove)
exports.removeFromCart = async (req, res) => {
    const { cartId } = req.params;

    try {
        const pool = await sql.connect();
        await pool.request()
            .input('id', sql.Int, cartId)
            .query(`DELETE FROM Carts WHERE cart_id = @id`);

        res.json({ message: 'Ürün silindi' });
    } catch (error) {
        console.error('Remove Cart Error:', error);
        res.status(500).json({ message: 'Silme başarısız.' });
    }
};
