import json
import re
from tqdm import tqdm


def parse_weight(weight_str):
    if not weight_str:
        return None
    match = re.search(r"([\d\.]+)\s*kg", weight_str.replace(",", "."))
    if match:
        return float(match.group(1))
    match = re.search(r"~([\d\.]+)", weight_str.replace(",", "."))
    if match:
        return float(match.group(1))
    return None


def parse_price(price_str):
    if not price_str:
        return None
    price = re.sub(r"[^\d]", "", price_str)
    return int(price) if price else None


def parse_screen_size(res_str):
    if not res_str:
        return None
    match = re.search(r'(\d{2}\.?\d*)[″"]', res_str)
    if match:
        return float(match.group(1))
    return None


def parse_resolution(res_str):
    if not res_str:
        return None
    match = re.search(r"(\d{3,4}\s*[x×]\s*\d{3,4})", res_str)
    if match:
        return match.group(1).replace(" ", "").replace("×", "x")
    return None


def parse_refresh_rate(res_str):
    if not res_str:
        return None
    match = re.search(r"(\d{2,3})\s*Hz", res_str)
    if match:
        return int(match.group(1))
    return None


def normalize_str(s):
    return s.replace("'", "''") if s else s


if __name__ == "__main__":
    with open("data_process/scrape/sazo_laptops.json", "r", encoding="utf-8") as f:
        laptops = json.load(f)

    laptop_rows = []
    cpu_rows = []
    ram_rows = []
    storage_rows = []
    screen_rows = []
    gpu_rows = []
    port_rows = []
    wireless_rows = []
    camera_rows = []
    keyboard_rows = []
    battery_rows = []
    material_rows = []
    warranty_rows = []
    os_rows = []
    physical_rows = []
    condition_rows = []

    for idx, item in enumerate(tqdm(laptops, desc="Processing laptops")):
        specs = item.get("specifications", {})
        laptop_id = idx + 1

        # CPU
        cpu_model = specs.get("CPU")
        cpu_id = f"cpu_{laptop_id}" if cpu_model else None
        if cpu_model:
            cpu_rows.append((cpu_id, normalize_str(cpu_model)))

        # RAM
        ram_model = specs.get("Ram")
        ram_id = f"ram_{laptop_id}" if ram_model else None
        if ram_model:
            ram_rows.append((ram_id, normalize_str(ram_model)))

        # Storage
        storage_model = specs.get("Ổ cứng")
        storage_id = f"storage_{laptop_id}" if storage_model else None
        if storage_model:
            storage_rows.append((storage_id, normalize_str(storage_model)))

        # Screen
        screen_model = specs.get("Độ phân giải")
        screen_id = f"screen_{laptop_id}" if screen_model else None
        if screen_model:
            screen_rows.append(
                (
                    screen_id,
                    parse_screen_size(screen_model),
                    normalize_str(parse_resolution(screen_model)),
                    parse_refresh_rate(screen_model),
                    normalize_str(screen_model),
                )
            )

        # Main laptop row
        laptop_rows.append(
            (
                laptop_id,
                normalize_str(item.get("title")),
                item.get("url"),
                parse_price(item.get("price")),
                item.get("brand"),
                parse_weight(specs.get("Trọng lượng")),
                cpu_id,
                ram_id,
                storage_id,
                screen_id,
                item.get("description"),
                item.get("image_url"),
                item.get("scraped_at"),
            )
        )

    # Example: print SQL INSERTs for laptops
    for row in laptop_rows:
        print(
            f"INSERT INTO laptops (id, title, url, price, brand, weight_kg, cpu_id, ram_id, storage_id, screen_id, description, image_url, scraped_at) VALUES {row};"
        )

    # Example: print SQL INSERTs for cpus
    for row in cpu_rows:
        print(f"INSERT INTO cpus (id, cpu_model) VALUES {row};")

    # Example: print SQL INSERTs for rams
    for row in ram_rows:
        print(f"INSERT INTO rams (id, ram_type) VALUES {row};")

    # Example: print SQL INSERTs for storages
    for row in storage_rows:
        print(f"INSERT INTO storages (id, storage_type) VALUES {row};")

    # Example: print SQL INSERTs for screens
    for row in screen_rows:
        print(
            f"INSERT INTO screens (id, size_inch, resolution, refresh_rate_hz, screen_desc) VALUES {row};"
        )
