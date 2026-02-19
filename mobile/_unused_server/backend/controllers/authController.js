const { sql } = require('../config/db');

exports.loginUser = async (req, res) => {
    const { email, password } = req.body;

    console.log('Login attempt:', { email, passwordProvided: !!password }); // Log 1

    try {
        if (!email || !password) {
            return res.status(400).json({ message: 'Email ve şifre gereklidir.' });
        }

        const pool = await sql.connect();
        // Log 2: Querying
        console.log('Querying database for:', email);

        const result = await pool.request()
            .input('email', sql.NVarChar, email)
            .query('SELECT customer_id, first_name, last_name, email, password_hash, segment FROM Customers WHERE email = @email');

        console.log('Query result count:', result.recordset.length); // Log 3

        if (result.recordset.length === 0) {
            console.log('User not found in DB');
            return res.status(401).json({ message: 'Kullanıcı bulunamadı.' });
        }

        const user = result.recordset[0];
        console.log('User found:', { dbEmail: user.email, dbHash: user.password_hash }); // Log 4

        // Demo amaçlı düz karşılaştırma (Production'da bcrypt kullanılmalı)
        // Trim whitespace just in case
        const dbPassword = user.password_hash ? user.password_hash.toString().trim() : '';
        const inputPassword = password.toString().trim();

        if (dbPassword !== inputPassword) {
            console.log('Password mismatch:', { db: dbPassword, input: inputPassword });
            return res.status(401).json({ message: 'Hatalı şifre.' });
        }

        // Hassas veriyi çıkar
        delete user.password_hash;

        res.json({
            message: 'Giriş başarılı',
            user: {
                id: user.customer_id,
                name: user.first_name,
                lastname: user.last_name,
                email: user.email,
                segment: user.segment
            }
        });

    } catch (error) {
        console.error('Login Error Full Details:', error);
        res.status(500).json({ message: 'Sunucu hatası.' });
    }
};
