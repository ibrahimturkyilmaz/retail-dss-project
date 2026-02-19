const sql = require('mssql');

const config = {
    server: process.env.DB_SERVER || 'localhost',
    database: process.env.DB_NAME || 'RetailDB',
    options: {
        encrypt: false, // Localde genellikle false olmalı
        trustServerCertificate: true,
        enableArithAbort: true
    }
};

// Veritabanı yapılandırması
// Eğer .env dosyasında kullanıcı adı/şifre varsa SQL Authentication kullanır.
// Yoksa, Windows Authentication (Trusted Connection) moduna geçer.
if (process.env.DB_USER && process.env.DB_PASSWORD) {
    config.user = process.env.DB_USER;
    config.password = process.env.DB_PASSWORD;
} else {
    config.options.trustedConnection = true;
}

const connectDB = async () => {
    try {
        console.log('Attempting connection with config:', {
            ...config,
            password: config.password ? '*****' : undefined
        });
        await sql.connect(config);
        console.log('SQL Server Connected Successfully');
    } catch (err) {
        console.error('Database Connection Failed! Details:', err);
        process.exit(1);
    }
};

module.exports = { connectDB, sql };
