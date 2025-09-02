import json
import re


def clean_string(s):
    """Convert string to valid OWL identifier format"""
    if not s:
        return ""
    # Remove special characters and replace spaces with underscores
    s = re.sub(r"[^a-zA-Z0-9\s]", "", s)
    return s.replace(" ", "_")


def extract_price(price_str):
    """Extract numeric price value from string"""
    if not price_str:
        return "0"
    return re.sub(r"[^\d]", "", price_str)


def parse_specifications(specs):
    """Convert specifications to OWL format specifications"""
    owl_specs = []

    # Map specifications to OWL format
    if specs.get("brand"):
        owl_specs.append(f":{clean_string(specs['brand'])}")

    if specs.get("CPU"):
        owl_specs.append(f":{clean_string(specs['CPU'])}")

    if specs.get("Ram"):
        owl_specs.append(f":{clean_string(specs['Ram'])}")

    if specs.get("Ổ cứng"):
        owl_specs.append(f":{clean_string(specs['Ổ cứng'])}")

    if specs.get("Độ phân giải"):
        resolution = specs["Độ phân giải"]
        # Extract resolution specs
        if "2560x1600" in resolution:
            owl_specs.append(":Resolution_2560x1600")
        if "nits" in resolution:
            nits = re.search(r"(\d+)nits", resolution)
            if nits:
                owl_specs.append(f":Brightness_{nits.group(1)}nits")
        if "Hz" in resolution:
            hz = re.search(r"(\d+)Hz", resolution)
            if hz:
                owl_specs.append(f":RefreshRate_{hz.group(1)}Hz")

    if specs.get("Pin"):
        owl_specs.append(f":Battery_{clean_string(specs['Pin'])}")

    if specs.get("Trọng lượng"):
        weight = specs["Trọng lượng"]
        if "kg" in weight:
            kg = re.search(r"~?(\d+\.?\d*)\s*kg", weight)
            if kg:
                owl_specs.append(f":Weight_{kg.group(1).replace('.', '_')}kg")

    return owl_specs


def json_to_owl(json_data):
    """Transform JSON data to OWL format"""
    owl_content = []

    for item in json_data:
        # Create product identifier from title
        product_id = clean_string(item["title"])

        # Start product definition
        owl_content.append(f":{product_id} rdf:type :Product ;")

        # Add specifications
        specs = parse_specifications(item.get("specifications", {}))
        if specs:
            owl_content.append(
                "    :hasSpecification "
                + " ,\n                      ".join(specs)
                + " ;"
            )

        # Add price
        price = extract_price(item["price"])
        owl_content.append(f'    :hasPrice "{price}"^^xsd:decimal .')

        owl_content.append("")  # Empty line between products

    return "\n".join(owl_content)


if __name__ == "__main__":
    # Read JSON file
    with open(
        "./data_process/scrape/sazo_laptops_enriched.json", "r", encoding="utf-8"
    ) as file:
        json_data = json.load(file)

    # Transform to OWL
    owl_output = json_to_owl(json_data)

    # Write output to file
    with open(
        "./data_process/process/owl_outputs/output.owl", "w", encoding="utf-8"
    ) as file:
        file.write(owl_output)
