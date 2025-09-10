import json
import re


def get_unique_items(data, key):
    """Extract unique items from a list of dictionaries based on a specified key"""
    unique_items = set()
    for item in data:
        if key in item:
            unique_items.add(item[key])
    return list(unique_items)


if __name__ == "__main__":
    # Read JSON file
    with open(
        "./data_process/scrape/sazo_laptops_enriched.json", "r", encoding="utf-8"
    ) as file:
        json_data = json.load(file)

    # Transform to OWL
    # owl_output = json_to_owl(json_data)
    unique_brands = get_unique_items(json_data, "specifications -> CPU")

    # Write output to file
    with open(
        "./data_process/process/owl_outputs/output.owl", "w", encoding="utf-8"
    ) as file:
        file.write(owl_output)

specifications = (
    {
        "CPU": "AMD_Ryzen_5_8545H",
        "Ram": "32GB_DDR5",
        "Storage": "1TB_NVME_M.2_SSD",
        "Resolution": "15.6_FHD_144hz_9ms_IPS",
        "RefreshRate": "144Hz",
        "Graphics Card": "NVIDIA_GeForce_RTX_5050_Laptop_GPU_6GB_GDDR7",
        "Charger": "200W",
        "Weight": "2.23_kg",
        "Pin": "70wh",
        "Brand": "HP",
        "Title": "Pavilion Gaming 15 2025 (R5-8545H| 32GB RAM| 1TB SSD| RTX 5050)",
    },
)
