
import json
import re
from urllib.parse import quote
import os.path

# --- 1. SETUP: Define Namespaces from our Ontology ---
# Not needed for Neo4j/Cypher, but keeping the prefix for node labels

# --- 2. INPUT DATA: Your list of scraped JSON objects ---
with open('sazo_laptops.json', 'r', encoding='utf-8') as f:
    laptops_data = json.load(f)

# --- 3. PARSING FUNCTIONS: To clean up the messy text data ---
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

# --- 4. MAIN SCRIPT: Build Cypher queries ---

def create_laptop_cypher(data):
    # Start with a clean database
    cypher_queries = [
        "// Clear existing data",
        "MATCH (n) DETACH DELETE n;",
        ""
    ]
    


    # Create constraints for unique IDs
    cypher_queries.extend([
        "// Create constraints",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Laptop) REQUIRE l.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (c:CPU) REQUIRE c.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (r:RAM) REQUIRE r.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Storage) REQUIRE s.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (g:GPU) REQUIRE g.id IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Screen) REQUIRE d.id IS UNIQUE;",
        ""
    ])

    # Process each laptop
    for laptop in data:
        # Create a unique identifier for the laptop
        safe_title = quote(laptop['title'])
        laptop_id = safe_title
        
        # Create Laptop node
        laptop_props = {
            "id": laptop_id,
            "title": laptop['title'],
            "url": laptop['url']
        }
        
        price = parse_price(laptop.get('price'))


        if price: laptop_props["price"] = price
        
        specs = laptop.get('specifications', {})
        weight = parse_weight(specs.get('Trọng lượng'))
        if weight: laptop_props["weightKg"] = weight
        
        # Convert properties to Cypher format
        laptop_props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in laptop_props.items()])
        
        # Create Laptop node query
        cypher_queries.append(f"CREATE (l:Laptop {{{laptop_props_str}}});")
        
        # CPU
        cpu_str = specs.get('CPU')
        if cpu_str:
            cpu_id = f"CPU_{laptop_id}"
            cpu_props = {"id": cpu_id, "cpuModel": cpu_str}
            
            cores = parse_cpu_cores(cpu_str)
            if cores: cpu_props["coreCount"] = cores
            
            cpu_props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in cpu_props.items()])
            cypher_queries.append(f"CREATE (c:CPU {{{cpu_props_str}}});")
            cypher_queries.append(f"MATCH (l:Laptop {{id: {json.dumps(laptop_id)}}}) "
                                 f"MATCH (c:CPU {{id: {json.dumps(cpu_id)}}}) "
                                 f"CREATE (l)-[:HAS_COMPONENT]->(c);")
        
        # RAM
        ram_str = specs.get('Ram')
        if ram_str:
            ram_id = f"RAM_{laptop_id}"
            ram_size, ram_type = parse_ram(ram_str)
            ram_props = {"id": ram_id}
            if ram_size: ram_props["ramSizeGB"] = ram_size
            if ram_type: ram_props["ramType"] = ram_type
            
            ram_props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in ram_props.items()])
            cypher_queries.append(f"CREATE (r:RAM {{{ram_props_str}}});")
            cypher_queries.append(f"MATCH (l:Laptop {{id: {json.dumps(laptop_id)}}}) "
                                 f"MATCH (r:RAM {{id: {json.dumps(ram_id)}}}) "
                                 f"CREATE (l)-[:HAS_COMPONENT]->(r);")
        
        # Storage
        storage_str = specs.get('Ổ cứng')
        if storage_str:
            storage_id = f"Storage_{laptop_id}"
            storage_size, storage_type = parse_storage(storage_str)
            storage_props = {"id": storage_id}
            if storage_size: storage_props["storageSizeGB"] = storage_size
            if storage_type: storage_props["storageType"] = storage_type
            
            storage_props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in storage_props.items()])
            cypher_queries.append(f"CREATE (s:Storage {{{storage_props_str}}});")
            cypher_queries.append(f"MATCH (l:Laptop {{id: {json.dumps(laptop_id)}}}) "
                                 f"MATCH (s:Storage {{id: {json.dumps(storage_id)}}}) "
                                 f"CREATE (l)-[:HAS_COMPONENT]->(s);")
        
        # GPU
        gpu_str = specs.get('Card màn hình')
        if gpu_str:
            gpu_id = f"GPU_{laptop_id}"
            gpu_model, is_dedicated = parse_gpu(gpu_str)
            gpu_props = {"id": gpu_id}
            if gpu_model: gpu_props["gpuModel"] = gpu_model
            if is_dedicated is not None: gpu_props["isDedicated"] = is_dedicated
            
            gpu_props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in gpu_props.items()])
            cypher_queries.append(f"CREATE (g:GPU {{{gpu_props_str}}});")
            cypher_queries.append(f"MATCH (l:Laptop {{id: {json.dumps(laptop_id)}}}) "
                                 f"MATCH (g:GPU {{id: {json.dumps(gpu_id)}}}) "
                                 f"CREATE (l)-[:HAS_COMPONENT]->(g);")
        
        # Screen
        screen_str = specs.get('Độ phân giải')
        if screen_str:
            screen_id = f"Screen_{laptop_id}"
            screen_size, refresh_rate = parse_screen(screen_str)
            screen_props = {"id": screen_id}
            if screen_size: screen_props["screenSizeInches"] = screen_size
            if refresh_rate: screen_props["refreshRateHz"] = refresh_rate
            
            screen_props_str = ", ".join([f"{k}: {json.dumps(v)}" for k, v in screen_props.items()])
            cypher_queries.append(f"CREATE (d:Screen {{{screen_props_str}}});")
            cypher_queries.append(f"MATCH (l:Laptop {{id: {json.dumps(laptop_id)}}}) "
                                 f"MATCH (d:Screen {{id: {json.dumps(screen_id)}}}) "
                                 f"CREATE (l)-[:HAS_COMPONENT]->(d);")
        
        # Add a blank line after each laptop for readability
        cypher_queries.append("")
    
    return "\n".join(cypher_queries)

# --- 5. EXECUTE and SAVE ---
if __name__ == "__main__":
    cypher_output = create_laptop_cypher(laptops_data)
    
    # base_dir = "D:/Study/Cao-hoc/ki-3/T6_CS2307.CH190-Cong-nghe-tri-thuc/seminar/code"
    base_dir = r""
    out_path = os.path.join(base_dir, "cipher_outputs", "neo4j_import.cypher")
    
    # ensure output folder exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # write cypher file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cypher_output)
        print(f"Cypher queries written to {out_path}")