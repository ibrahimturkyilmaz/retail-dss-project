-- =============================================
-- MOBILE APP EXTENSION SCRIPT (FIXED VERSION)
-- Description: Adds Authentication, Cart, and Favorites features.
-- Includes fixes for existing data conflicts.
-- =============================================

-- 1. EXTEND CUSTOMERS (Authentication)
-- Adım 1: Kolonları kısıtlamasız (Constraint olmadan) ekle
IF COL_LENGTH('Customers', 'email') IS NULL
BEGIN
    ALTER TABLE Customers
    ADD email NVARCHAR(100);
END

IF COL_LENGTH('Customers', 'password_hash') IS NULL
BEGIN
    ALTER TABLE Customers
    ADD password_hash NVARCHAR(255);
END
GO

-- Adım 2: Mevcut verilerdeki NULL değerleri temizle (UNIQUE hatasını önlemek için)
-- Eğer tabloda müşteri varsa, email'i boş olanlara geçici mail ata
UPDATE Customers 
SET email = CAST(customer_id AS NVARCHAR(50)) + '@temp-placeholder.com' 
WHERE email IS NULL;
GO

-- Adım 3: Şimdi UNIQUE index oluştur
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='IX_Customers_Email' AND object_id = OBJECT_ID('Customers'))
BEGIN
    CREATE UNIQUE INDEX IX_Customers_Email ON Customers(email);
END
GO

-- 2. CARTS (Mobil Sepet Yönetimi)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Carts' AND xtype='U')
CREATE TABLE Carts (
    cart_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id NVARCHAR(50) NOT NULL,
    inventory_id NVARCHAR(50) NOT NULL,
    quantity INT DEFAULT 1,
    added_at DATETIME2 DEFAULT GETDATE(),

    CONSTRAINT FK_Carts_Customers FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    CONSTRAINT FK_Carts_Inventory FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id)
);
GO

-- 3. FAVORITES (Favori Ürünler)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Favorites' AND xtype='U')
CREATE TABLE Favorites (
    favorite_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id NVARCHAR(50) NOT NULL,
    product_id NVARCHAR(50) NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),

    CONSTRAINT FK_Favorites_Customers FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    CONSTRAINT FK_Favorites_Products FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
GO

-- =============================================
-- DEMO DATA INJECTION
-- =============================================

-- Demo Customer
-- ID çakışmasını önlemek için kontrol et
IF NOT EXISTS (SELECT * FROM Customers WHERE customer_id = 'CUST-DEMO-001')
BEGIN
    INSERT INTO Customers (customer_id, first_name, last_name, email, password_hash, segment)
    VALUES ('CUST-DEMO-001', 'Demo', 'User', 'demo@stylestore.com', '123456', 'VIP');
END
ELSE
BEGIN
    -- Eğer kullanıcı varsa ama emaili farklıysa güncelle
    UPDATE Customers SET email = 'demo@stylestore.com', password_hash = '123456' WHERE customer_id = 'CUST-DEMO-001';
END

-- Ensure 'Products' exists 
IF NOT EXISTS (SELECT * FROM Products WHERE product_id = 'PRD-001')
BEGIN
    INSERT INTO Products (product_id, product_name, category, price)
    VALUES ('PRD-001', 'Vintage Denim Jacket', 'Outerwear', 1250.00);
END

-- Ensure 'Stores' exists 
IF NOT EXISTS (SELECT * FROM Stores WHERE store_id = 'ST-001')
BEGIN
    INSERT INTO Stores (store_id, store_name, latitude, longitude)
    VALUES ('ST-001', 'Nişantaşı Flagship', 41.0522, 28.9959);
END

-- Create Inventory Link
IF NOT EXISTS (SELECT * FROM Inventory WHERE inventory_id = 'INV-001')
BEGIN
    INSERT INTO Inventory (inventory_id, store_id, product_id, stock_quantity)
    VALUES ('INV-001', 'ST-001', 'PRD-001', 50);
END
GO
