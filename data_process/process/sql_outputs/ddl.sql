-- Drop tables if they exist to allow for a clean run
DROP TABLE IF EXISTS screens;
DROP TABLE IF EXISTS storages;
DROP TABLE IF EXISTS rams;
DROP TABLE IF EXISTS cpus;
DROP TABLE IF EXISTS laptops;

-- Main laptops table
CREATE TABLE laptops (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    specifications JSON, -- For storing detailed specs
    image_url VARCHAR(500),
    stock_quantity INT DEFAULT 0,
    category TEXT,
    processor TEXT,
    ram TEXT,
    storage TEXT,
    graphics_card TEXT,
    screen_size TEXT,
    operating_system TEXT,
    weight DECIMAL(4, 2),
    battery_life TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);