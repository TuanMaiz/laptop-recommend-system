import os
import json
import re
from rdflib import Graph, Namespace, Literal, RDF, XSD

# === File Path ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "..", "scrape", "sazo_laptops.json")

# === RDF Namespace ===
EX = Namespace("http://example.org/laptop#")
g = Graph()
g.bind("ex", EX)

# === Helpers ===
def normalize(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '_', text.strip())

def parse_price(price_str: str):
    if not price_str:
        return None
    num = re.sub(r"[^\d]", "", price_str)
    return int(num) if num else None

# --- Regex Extractors ---
def extract_cpu(text):
    m = re.search(r"(Intel|AMD)\s+[A-Za-z0-9\s\-]+", text, re.I)
    return normalize(m.group(0)) if m else normalize(text)

def extract_ram(text):
    m = re.search(r"(\d+GB)\s+(DDR\d)(?:[- ](\d+MHz))?", text, re.I)
    if m:
        size, ddr, speed = m.groups()
        return f"RAM_{size}_{ddr}_{speed}" if speed else f"RAM_{size}_{ddr}"
    return normalize("RAM_" + text)

def extract_storage(text):
    m = re.search(r"(\d+(?:TB|GB)).*(SSD|HDD|NVMe)", text, re.I)
    if m:
        size, stype = m.groups()
        return f"Storage_{size}_{stype.upper()}"
    return normalize("Storage_" + text)

def extract_resolution(text):
    m = re.search(r"(\d{3,4}x\d{3,4})", text)
    return f"Resolution_{m.group(1)}" if m else normalize("Resolution_" + text)

def extract_brightness(text):
    m = re.search(r"(\d+)\s*nits", text, re.I)
    return f"Brightness_{m.group(1)}nits" if m else normalize("Brightness_" + text)

def extract_refresh(text):
    m = re.search(r"(\d{2,3})\s*Hz", text, re.I)
    return f"RefreshRate_{m.group(1)}Hz" if m else normalize("RefreshRate_" + text)

def extract_screen(text):
    m = re.search(r"(\d{2}\.?\d*)\s*inch", text, re.I)
    return f"ScreenSize_{m.group(1)}inch" if m else normalize("ScreenSize_" + text)

def extract_weight(text):
    m = re.search(r"(\d+\.?\d*)\s*kg", text, re.I)
    return f"Weight_{m.group(1)}kg" if m else normalize("Weight_" + text)

def extract_battery(text):
    m = re.search(r"(\d+Wh)", text, re.I)
    return f"Battery_{m.group(1)}" if m else normalize("Battery_" + text)

# === Load JSON ===
with open(FILE_PATH, "r", encoding="utf-8") as f:
    laptops = json.load(f)

# === Process Laptops ===
for data in laptops:
    product_id = normalize(data["title"])
    product = EX[product_id]
    g.add((product, RDF.type, EX.Product))

    # Brand
    if data.get("brand"):
        brand_ind = EX[normalize(data["brand"])]
        g.add((brand_ind, RDF.type, EX.Brand))
        g.add((product, EX.hasSpecification, brand_ind))

    # Price
    price_val = parse_price(data.get("price"))
    if price_val:
        g.add((product, EX.hasPrice, Literal(price_val, datatype=XSD.decimal)))

    specs = data.get("specifications", {})

    if "CPU" in specs:
        cpu_ind = EX[extract_cpu(specs["CPU"])]
        g.add((cpu_ind, RDF.type, EX.CPU))
        g.add((product, EX.hasSpecification, cpu_ind))

    if "Ram" in specs:
        ram_ind = EX[extract_ram(specs["Ram"])]
        g.add((ram_ind, RDF.type, EX.RAM))
        g.add((product, EX.hasSpecification, ram_ind))

    if "Ổ cứng" in specs:
        storage_ind = EX[extract_storage(specs["Ổ cứng"])]
        g.add((storage_ind, RDF.type, EX.Storage))
        g.add((product, EX.hasSpecification, storage_ind))

    if "Độ phân giải" in specs:
        res_ind = EX[extract_resolution(specs["Độ phân giải"])]
        g.add((res_ind, RDF.type, EX.Resolution))
        g.add((product, EX.hasSpecification, res_ind))

    if "Độ sáng" in specs:
        bright_ind = EX[extract_brightness(specs["Độ sáng"])]
        g.add((bright_ind, RDF.type, EX.Brightness))
        g.add((product, EX.hasSpecification, bright_ind))

    if "Tần số quét" in specs:
        hz_ind = EX[extract_refresh(specs["Tần số quét"])]
        g.add((hz_ind, RDF.type, EX.Refresh_rate))
        g.add((product, EX.hasSpecification, hz_ind))

    if "Màn hình" in specs:
        size_ind = EX[extract_screen(specs["Màn hình"])]
        g.add((size_ind, RDF.type, EX.Screen_size))
        g.add((product, EX.hasSpecification, size_ind))

    if "Trọng lượng" in specs:
        weight_ind = EX[extract_weight(specs["Trọng lượng"])]
        g.add((weight_ind, RDF.type, EX.Weight))
        g.add((product, EX.hasSpecification, weight_ind))

    if "Pin" in specs:
        battery_ind = EX[extract_battery(specs["Pin"])]
        g.add((battery_ind, RDF.type, EX.Battery))
        g.add((product, EX.hasSpecification, battery_ind))

# === Save Ontology ===
OUTPUT_PATH = os.path.join(BASE_DIR, "laptops_clean.owl")
g.serialize(OUTPUT_PATH, format="turtle")
print(f"✅ Clean OWL ontology exported to {OUTPUT_PATH}")
