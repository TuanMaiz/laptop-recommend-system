import json
from .item_map import (
    CPU_MAP,
    RAM_MAP,
    STORAGE_MAP,
    BATTERIES_MAP,
    GPU_MAP,
    SCREEN_MAP,
    RESOLUTION_MAP,
    REFRESH_RATE_MAP,
    BRIGHTNESS_MAP,
    WEIGHT_MAP,
)


def get_unique_items_from_json(key):
    """Extract unique items from a list of dictionaries based on a specified key"""
    # Read JSON file
    with open(
        "./data_process/scrape/sazo_laptops_enriched.json", "r", encoding="utf-8"
    ) as file:
        json_data = json.load(file)
    unique_items = set()
    for item in json_data:
        if key in item:
            unique_items.add(item[key])
    return list(unique_items)


def get_unique_items_from_item_map():
    result = {}
    for map, label in [
        (CPU_MAP, "CPU"),
        (RAM_MAP, "RAM"),
        (STORAGE_MAP, "STORAGE"),
        (BATTERIES_MAP, "BATTERY"),
        (GPU_MAP, "GPU"),
        (SCREEN_MAP, "SCREEN"),
        (RESOLUTION_MAP, "RESOLUTION"),
        (REFRESH_RATE_MAP, "REFRESH_RATE"),
        (BRIGHTNESS_MAP, "BRIGHTNESS"),
        (WEIGHT_MAP, "WEIGHT"),
    ]:
        unique_items = set()
        for k, v in map.items():
            if v not in unique_items:
                unique_items.add(v)
        result[label] = list(unique_items)

    with open(
        "./data_process/process/sub_process/unique_key_tmp.json", "a", encoding="utf-8"
    ) as file:
        file.write(json.dumps(result, indent=4))
    return list(unique_items)


def group_items_by_category(items, category_map):
    with open(
        "./data_process/process/sub_process/unique_key.json", "r", encoding="utf-8"
    ) as file:
        json_data = json.load(file)
    categorized_items = {}
    for item in [json_data["CPU"], json_data["GPU"], json_data["RAM"]]:
        for k, v in item.items():
            if "Gaming" in v:
                category_map["Gaming"] = k
            elif "Office" in v:
                category_map["Office"] = k
            else:
                category_map["Graphic"] = k

    return categorized_items


if __name__ == "__main__":

    # Transform to OWL
    # owl_output = json_to_owl(json_data)
    # unique_brands = get_unique_items_from_json("specifications -> CPU")
    get_unique_items_from_item_map()
