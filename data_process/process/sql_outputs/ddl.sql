-- Drop tables if they exist to allow for a clean run
DROP TABLE IF EXISTS screens;
DROP TABLE IF EXISTS storages;
DROP TABLE IF EXISTS rams;
DROP TABLE IF EXISTS cpus;
DROP TABLE IF EXISTS laptops;

-- Main laptops table
CREATE TABLE laptops (
    id INTEGER PRIMARY KEY,
    title TEXT,
    url TEXT,
    price NUMERIC,
    brand TEXT,
    weight_kg NUMERIC(5,2),
    description TEXT,
    image_url TEXT,
    scraped_at TIMESTAMP
);

-- CPUs table (normalized)
CREATE TABLE cpus (
    id TEXT PRIMARY KEY,
    cpu_model TEXT,
    core_count INTEGER,
    thread_count INTEGER,
    base_clock_ghz NUMERIC(4,2),
    boost_clock_ghz NUMERIC(4,2),
    cache_mb NUMERIC(4,1),
    brand TEXT
);

-- RAMs table (normalized)
CREATE TABLE rams (
    id TEXT PRIMARY KEY,
    ram_size_gb INTEGER,
    ram_type VARCHAR(50),
    upgradeable BOOLEAN,
    speed_mhz INTEGER
);

-- Storages table (normalized)
CREATE TABLE storages (
    id TEXT PRIMARY KEY,
    storage_size_gb INTEGER,
    storage_type VARCHAR(50),
    interface TEXT
);

-- Screens table (normalized)
CREATE TABLE screens (
    id TEXT PRIMARY KEY,
    size_inch NUMERIC(4,1),
    resolution TEXT,
    panel_type TEXT,
    refresh_rate_hz INTEGER,
    brightness_nits INTEGER,
    color_gamut TEXT,
    touch BOOLEAN
);

-- GPUs table (normalized)
CREATE TABLE gpus (
    id TEXT PRIMARY KEY,
    gpu_model TEXT,
    vram_gb INTEGER,
    is_dedicated BOOLEAN
);

-- Link main laptop to its components (foreign keys)
ALTER TABLE laptops
    ADD COLUMN cpu_id TEXT REFERENCES cpus(id),
    ADD COLUMN ram_id TEXT REFERENCES rams(id),
    ADD COLUMN storage_id TEXT REFERENCES storages(id),
    ADD COLUMN screen_id TEXT REFERENCES screens(id),
    ADD COLUMN gpu_id TEXT REFERENCES gpus(id);