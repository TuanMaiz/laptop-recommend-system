import json
import re
from rdflib import Graph, Namespace, URIRef, Literal, RDF, XSD
from urllib.parse import quote
import os.path
# --- 1. SETUP: Define Namespaces from our Ontology ---
# This ensures our output uses the same vocabulary we designed.
LOPT = Namespace("http://www.abacus.ai/ontologies/laptop#")

# --- 2. INPUT DATA: Your list of scraped JSON objects ---
# In a real application, you would load this from a file:
# with open('your_data.json', 'r') as f:
#     laptops_data = json.load(f)

with open('sazo_laptops.json', 'r', encoding='utf-8') as f:
    laptops_data = json.load(f)

# --- 3. PARSING FUNCTIONS: To clean up the messy text data ---
# These functions use regular expressions (regex) to find the data we need.
# They are designed to be robust, returning None if a value can't be found.
def parse_brand(brand_str):
    if not brand_str: return None
    return brand_str.strip()

def parse_price(price_str):
    if not price_str: return None
    return float(''.join(re.findall(r'\d+', price_str)))

def parse_ram(ram_str):
    if not ram_str: return None, None
    size_match = re.search(r'(\d+)GB', ram_str)
    type_match = re.search(r'(DDR\d+)', ram_str)
    size = int(size_match.group(1)) if size_match else None
    ram_type = type_match.group(1) if type_match else None
    return size, ram_type

def parse_storage(storage_str):
    if not storage_str: return None, None
    size_gb = None
    if 'TB' in storage_str:
        size_match = re.search(r'(\d+)\s*TB', storage_str)
        if size_match: size_gb = int(size_match.group(1)) * 1024
    elif 'GB' in storage_str:
        size_match = re.search(r'(\d+)\s*GB', storage_str)
        if size_match: size_gb = int(size_match.group(1))
    
    storage_type = "SSD" if "SSD" in storage_str else "HDD" if "HDD" in storage_str else None
    return size_gb, storage_type

def parse_gpu(gpu_str):
    if not gpu_str: return None, None
    # Heuristic: if it says "onboard", "integrated", or is a common Intel integrated model, it's not dedicated.
    is_dedicated = not any(keyword in gpu_str.lower() for keyword in ["onboard", "integrated", "intel hd", "iris xe"])
    return gpu_str, is_dedicated

def parse_screen(screen_str):
    if not screen_str: return None, None
    size_match = re.search(r'(\d+\.?\d*)"', screen_str)
    refresh_match = re.search(r'(\d+)\s*Hz', screen_str)
    size = float(size_match.group(1)) if size_match else None
    refresh_rate = int(refresh_match.group(1)) if refresh_match else None
    return size, refresh_rate

def parse_weight(weight_str):
    if not weight_str: return None
    match = re.search(r'(\d+\.?\d*)', weight_str)
    return float(match.group(1)) if match else None

def parse_cpu_cores(cpu_str):
    if not cpu_str: return None
    match = re.search(r'(\d+)\s*nhân', cpu_str) # "nhân" is Vietnamese for "core"
    return int(match.group(1)) if match else None

# --- 4. MAIN SCRIPT: Build the Graph ---

def create_laptop_graph(data):
    g = Graph()
    g.bind("lopt", LOPT) # Binds the prefix for cleaner output

    for laptop in data:
        # Create a unique, URL-safe identifier for the laptop
        safe_title = quote(laptop['title'])
        laptop_uri = LOPT[safe_title]

        # Add the core triple: This URI represents an instance of the Laptop class
        g.add((laptop_uri, RDF.type, LOPT.Laptop))

        # Add Data Properties for the Laptop
        g.add((laptop_uri, LOPT.hasTitle, Literal(laptop['title'], datatype=XSD.string)))
        g.add((laptop_uri, LOPT.hasUrl, Literal(laptop['url'], datatype=XSD.anyURI)))
        
        price = parse_price(laptop.get('price'))
        if price: g.add((laptop_uri, LOPT.hasPrice, Literal(price, datatype=XSD.float)))
        
        specs = laptop.get('specifications', {})
        weight = parse_weight(specs.get('Trọng lượng'))
        if weight: g.add((laptop_uri, LOPT.hasWeightKg, Literal(weight, datatype=XSD.float)))

        # --- Create and link Component instances ---

        # CPU
        cpu_str = specs.get('CPU')
        if cpu_str:
            cpu_uri = LOPT[f"CPU_{safe_title}"]
            g.add((laptop_uri, LOPT.hasComponent, cpu_uri))
            g.add((cpu_uri, RDF.type, LOPT.CPU))
            g.add((cpu_uri, LOPT.hasCpuModel, Literal(cpu_str, datatype=XSD.string)))
            cores = parse_cpu_cores(cpu_str)
            if cores: g.add((cpu_uri, LOPT.hasCoreCount, Literal(cores, datatype=XSD.integer)))

        # RAM
        ram_str = specs.get('Ram')
        if ram_str:
            ram_uri = LOPT[f"RAM_{safe_title}"]
            ram_size, ram_type = parse_ram(ram_str)
            g.add((laptop_uri, LOPT.hasComponent, ram_uri))
            g.add((ram_uri, RDF.type, LOPT.RAM))
            if ram_size: g.add((ram_uri, LOPT.hasRamSizeGB, Literal(ram_size, datatype=XSD.integer)))
            if ram_type: g.add((ram_uri, LOPT.hasRamType, Literal(ram_type, datatype=XSD.string)))

        # Storage
        storage_str = specs.get('Ổ cứng')
        if storage_str:
            storage_uri = LOPT[f"Storage_{safe_title}"]
            storage_size, storage_type = parse_storage(storage_str)
            g.add((laptop_uri, LOPT.hasComponent, storage_uri))
            g.add((storage_uri, RDF.type, LOPT.Storage))
            if storage_size: g.add((storage_uri, LOPT.hasStorageSizeGB, Literal(storage_size, datatype=XSD.integer)))
            if storage_type: g.add((storage_uri, LOPT.hasStorageType, Literal(storage_type, datatype=XSD.string)))

        # GPU
        gpu_str = specs.get('Card màn hình')
        if gpu_str:
            gpu_uri = LOPT[f"GPU_{safe_title}"]
            gpu_model, is_dedicated = parse_gpu(gpu_str)
            g.add((laptop_uri, LOPT.hasComponent, gpu_uri))
            g.add((gpu_uri, RDF.type, LOPT.GPU))
            if gpu_model: g.add((gpu_uri, LOPT.hasGpuModel, Literal(gpu_model, datatype=XSD.string)))
            if is_dedicated is not None: g.add((gpu_uri, LOPT.isDedicatedGpu, Literal(is_dedicated, datatype=XSD.boolean)))

        # Screen
        screen_str = specs.get('Độ phân giải')
        if screen_str:
            screen_uri = LOPT[f"Screen_{safe_title}"]
            screen_size, refresh_rate = parse_screen(screen_str)
            g.add((laptop_uri, LOPT.hasComponent, screen_uri))
            g.add((screen_uri, RDF.type, LOPT.Screen))
            if screen_size: g.add((screen_uri, LOPT.hasScreenSizeInches, Literal(screen_size, datatype=XSD.float)))
            if refresh_rate: g.add((screen_uri, LOPT.hasRefreshRateHz, Literal(refresh_rate, datatype=XSD.integer)))

    return g.serialize(format="turtle")

# --- 5. EXECUTE and PRINT ---
if __name__ == "__main__":
    turtle_output = create_laptop_graph(laptops_data)

    # base_dir = r"D:/Study/Cao-hoc/ki-3/T6_CS2307.CH190-Cong-nghe-tri-thuc/seminar/code"
    base_dir = r""
    ontology_path = os.path.join(base_dir, "ontology.ttl")
    out_path      = os.path.join(base_dir, "outputs", "ontology+instances.ttl")

    # read existing ontology
    with open(ontology_path, "r", encoding="utf‑8") as f:
        ontology_text = f.read()

    # merge: ontology first, then generated instances
    merged = ontology_text.rstrip() + "\n\n" + turtle_output.lstrip()

    # ensure output folder exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # write combined file
    with open(out_path, "w", encoding="utf‑8") as f:
        f.write(merged)
    
    #print(turtle_output)