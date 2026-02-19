-- =============================================
-- Database Update Script for Retail App Mobile Features
-- Target System: Microsoft SQL Server
-- Description: Creates tables for Segmentation, Multi-store Inventory, and Order History.
-- =============================================

-- 1. SEGMENTS (Müşteri Segmentleri)
-- Kullanıcıları "VIP", "Yeni", "Vintage Sever" gibi gruplara ayırır.
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Segments' AND xtype='U')
CREATE TABLE Segments (
    SegmentID INT IDENTITY(1,1) PRIMARY KEY,
    SegmentName NVARCHAR(50) NOT NULL, -- Örn: 'VIP', 'Student', 'VintageLover'
    DiscountRate DECIMAL(5, 2) DEFAULT 0.00, -- Örn: 0.10 (%10 indirim)
    Description NVARCHAR(255)
);

-- 2. USERS (Kullanıcılar)
-- SegmentID ile segment tablosuna bağlanır.
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL, -- Gerçek uygulamada hashlenmeli
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    SegmentID INT FOREIGN KEY REFERENCES Segments(SegmentID),
    CreatedAt DATETIME DEFAULT GETDATE()
);

-- 3. STORES (Mağazalar)
-- Coğrafi konum ve özellik bilgileri.
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Stores' AND xtype='U')
CREATE TABLE Stores (
    StoreID INT IDENTITY(1,1) PRIMARY KEY,
    StoreName NVARCHAR(100) NOT NULL,
    Latitude DECIMAL(9, 6),
    Longitude DECIMAL(9, 6),
    Address NVARCHAR(max),
    Features NVARCHAR(max) -- JSON olarak özellikler saklanabilir: '["Wifi", "Cafe"]'
);

-- 4. PRODUCTS (Ürün Kataloğu)
-- Ürünlerin genel tanımları.
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Products' AND xtype='U')
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Category NVARCHAR(50), -- 'Outerwear', 'Accessories'
    BasePrice DECIMAL(10, 2) NOT NULL,
    ImageURL NVARCHAR(max),
    TargetSegmentID INT FOREIGN KEY REFERENCES Segments(SegmentID) -- Hangi segmente hitap ediyor?
);

-- 5. INVENTORY (Mağaza Bazlı Stok ve Fiyat)
-- "Her mağazada farklı ürünler olabilir" kuralı için.
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Inventory' AND xtype='U')
CREATE TABLE Inventory (
    InventoryID INT IDENTITY(1,1) PRIMARY KEY,
    StoreID INT FOREIGN KEY REFERENCES Stores(StoreID),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    StockQuantity INT DEFAULT 0,
    IsAvailable BIT DEFAULT 1,
    LocalPrice DECIMAL(10, 2) -- Mağazaya özel fiyat olabilir
);

-- 6. ORDERS (Sipariş Geçmişi)
-- Müşterinin eski alışverişleri.
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Orders' AND xtype='U')
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    OrderDate DATETIME DEFAULT GETDATE(),
    TotalAmount DECIMAL(10, 2),
    Status NVARCHAR(20) DEFAULT 'Completed' -- 'Pending', 'Completed', 'Returned'
);

-- 7. ORDER_DETAILS (Sipariş Detayı)
-- Hangi mağazadan hangi ürün alındı?
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='OrderDetails' AND xtype='U')
CREATE TABLE OrderDetails (
    DetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    InventoryID INT FOREIGN KEY REFERENCES Inventory(InventoryID), -- Hangi mağazadaki ürünü aldı?
    Quantity INT DEFAULT 1,
    UnitPrice DECIMAL(10, 2)
);

-- 8. CARTS (Aktif Sepet)
-- Kullanıcının o anki sepeti. Persistent (kalıcı) sepet için.
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Carts' AND xtype='U')
CREATE TABLE Carts (
    CartID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    InventoryID INT FOREIGN KEY REFERENCES Inventory(InventoryID),
    Quantity INT DEFAULT 1,
    AddedAt DATETIME DEFAULT GETDATE()
);

-- =============================================
-- SAMPLE DATA INSERTION (Demo Verileri)
-- =============================================

-- Segments
INSERT INTO Segments (SegmentName, DiscountRate, Description) VALUES 
('Standart', 0.00, 'Yeni veya sisteme girmemiş kullanıcı'),
('VIP', 0.15, 'Sadık müşteri, %15 indirim'),
('VintageLover', 0.05, 'Retro ürün alıcısı');

-- Users
INSERT INTO Users (Email, PasswordHash, FirstName, LastName, SegmentID) VALUES
('demo@stylestore.com', '123456', 'Demo', 'Kullanıcı', 2); -- VIP User

-- Stores
INSERT INTO Stores (StoreName, Latitude, Longitude, Address) VALUES
('Nişantaşı Flagship', 41.0522, 28.9959, 'Teşvikiye Mah. Şişli'),
('Kadıköy Concept', 40.9901, 29.0298, 'Caferağa Mah. Kadıköy');

-- Products
INSERT INTO Products (Name, Category, BasePrice, ImageURL, TargetSegmentID) VALUES
('Vintage Denim Jacket', 'Outerwear', 1250.00, 'https://example.com/jacket.jpg', 3),
('Oversized Hoodie', 'Tops', 850.00, 'https://example.com/hoodie.jpg', 1);

-- Inventory (Multi-store setup)
-- Nişantaşı has both
INSERT INTO Inventory (StoreID, ProductID, StockQuantity) VALUES (1, 1, 10), (1, 2, 50);
-- Kadıköy only has Hoodie
INSERT INTO Inventory (StoreID, ProductID, StockQuantity) VALUES (2, 2, 20);
