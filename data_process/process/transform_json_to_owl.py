import json
import re
from enum import Enum
from .sub_process.item_map import (
    CPU_MAP,
    RAM_MAP,
    GPU_MAP,
    STORAGE_MAP,
    BRIGHTNESS_MAP,
    REFRESH_RATE_MAP,
    WEIGHT_MAP,
    BATTERIES_MAP,
    RESOLUTION_MAP,
    SCREEN_MAP,
)

# from transformers import pipeline

# qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


class ResolutionSubInfo(Enum):
    BRIGHTNESS = "brightness"
    REFRESH_RATE = "refresh_rate"
    RESOLUTION = "resolution"
    SCREEN_SIZE = "screen_size"


class AggregateData:
    @staticmethod
    def get_resolution_subinfo(product, info_key, matched_group=None):
        result = ""
        specs = product.get("specifications", {})
        _item = None

        # Build pattern
        if info_key == ResolutionSubInfo.BRIGHTNESS.value:
            pattern = r"(\d+)\s*nits"
            unit = "nits"
        elif info_key == ResolutionSubInfo.REFRESH_RATE.value:
            pattern = r"(\d+)\s*Hz"
            unit = ""
        elif info_key == ResolutionSubInfo.RESOLUTION.value:
            pattern = r"\b\d{3,4}\s*[x×]\s*\d{3,4}\b"
            unit = ""
        elif info_key == ResolutionSubInfo.SCREEN_SIZE.value:
            pattern = r'\b\d{1,2}(\.\d{1,2})?\s*(?:["″]|-?inch)\b'
            unit = ""

        value = specs.get("Độ phân giải") or specs.get("Resolution")
        if value:
            if isinstance(value, str) and re.search(pattern, value, re.IGNORECASE):
                match = re.search(pattern, value, re.IGNORECASE)
                if match:
                    result = (
                        match.group(matched_group)
                        if matched_group
                        else match.group() + unit
                    )

        return result

    @staticmethod
    def execute():
        with open(
            "./data_process/scrape/sazo_laptops_enriched.json", "r", encoding="utf-8"
        ) as file:
            json_data = json.load(file)

        cpus = set()
        rams = set()
        gpus = set()
        storages = set()
        resolutions = set()
        brightness = set()
        screen_size = set()
        refresh_rate = set()
        weight = set()
        batteries = set()
        for _data in json_data:
            cpus.add(_data.get("specifications", {}).get("CPU", ""))
            rams.add(_data.get("specifications", {}).get("Ram", ""))
            gpus.add(_data.get("specifications", {}).get("Card màn hình", ""))
            storages.add(_data.get("specifications", {}).get("Ổ cứng", ""))
            resolutions.add(
                AggregateData.get_resolution_subinfo(
                    _data, ResolutionSubInfo.RESOLUTION.value
                )
            )
            # brightness.add(_data.get("specifications", {}).get("Độ phân giải", ""))
            brightness.add(
                AggregateData.get_resolution_subinfo(
                    _data, ResolutionSubInfo.BRIGHTNESS.value, 1
                )
            )
            # refresh_rate.add(_data.get("specifications", {}).get("Độ phân giải", ""))
            refresh_rate.add(
                AggregateData.get_resolution_subinfo(
                    _data, ResolutionSubInfo.REFRESH_RATE.value, 1
                )
            )
            screen_size.add(
                AggregateData.get_resolution_subinfo(
                    _data, ResolutionSubInfo.SCREEN_SIZE.value
                )
            )
            weight.add(_data.get("specifications", {}).get("Trọng lượng", ""))
            batteries.add(_data.get("specifications", {}).get("Sạc", ""))

        with open(
            "./data_process/process/sub_process/unique_specs.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.write("CPUs:\n" + "\n".join(sorted(cpus)) + "\n")
            file.write("RAMs:\n" + "\n".join(sorted(rams)) + "\n")
            file.write("GPUs:\n" + "\n".join(sorted(gpus)) + "\n")
            file.write("Storage:\n" + "\n".join(sorted(storages)) + "\n")
            file.write("Resolution:\n" + "\n".join(sorted(resolutions)) + "\n")
            file.write("Brightness:\n" + "\n".join(sorted(brightness)) + "\n")
            file.write("Refresh rate:\n" + "\n".join(sorted(refresh_rate)) + "\n")
            file.write("Screen size:\n" + "\n".join(sorted(screen_size)) + "\n")
            file.write("Weight:\n" + "\n".join(sorted(weight)) + "\n")
            file.write("Batteries:\n" + "\n".join(sorted(batteries)) + "\n")


class ParseOtherEntitiesJSONToOWL:
    @staticmethod
    def cpu_entity(id: str, raw: str) -> str:
        brand = "AMD" if "AMD" in raw else "Intel" if "Intel" in raw else "Unknown"
        model = (
            raw.replace("AMD", "").replace("Intel", "").replace("Processor", "").strip()
        )
        model = re.sub(r"\(.*?\)", "", model).strip()

        cores = re.search(r"(\d+)\s*(?:cores?|nhân)", raw)
        threads = re.search(r"(\d+)\s*(?:threads?|luồng)", raw)
        base = re.search(r"base clock\s*([\d\.]+)\s*GHz", raw, re.I)
        boost = re.search(r"up to\s*([\d\.]+)\s*GHz", raw, re.I)
        cache = re.search(r"(\d+MB)\s+(?:L3|Cache)", raw, re.I)
        if not cache:
            cache = re.search(r"(\d+MB)\s+(?:\w+\s+)*", raw, re.I)

        return f"""
        :{id} rdf:type :CPU ;
            :brand "{brand}" ;
            :model "{model}" ;
            :cores "{cores.group(1) if cores else '?'}"^^xsd:integer ;
            :threads "{threads.group(1) if threads else '?'}"^^xsd:integer ;
            :baseClock "{base.group(1)+'GHz' if base else '?'}" ;
            :boostClock "{boost.group(1)+'GHz' if boost else '?'}" ;
            :cache "{cache.group(1) if cache else '?'}" .
        """

    @staticmethod
    def ram_entity(id: str, raw: str) -> str:
        cap = re.search(r"(\d+)\s*GB", raw, re.I)
        type_ = re.search(r"(DDR\d(?:-\d+)?)", raw, re.I)
        speed = re.search(r"(\d+)\s*MHz", raw, re.I)
        up = "true" if "upgradeable" in raw.lower() else "false"

        return f"""
        :{id} rdf:type :RAM ;
            :capacity "{cap.group(1) if cap else '?'}"^^xsd:integer ;
            :type "{type_.group(1) if type_ else '?'}" ;
            :speed "{speed.group(1)+'MHz' if speed else '?'}" ;
            :upgradeable "{up}"^^xsd:boolean .
        """

    @staticmethod
    def gpu_entity(id: str, raw: str) -> str:
        brand = (
            "NVIDIA"
            if "NVIDIA" in raw
            else "AMD" if "AMD" in raw else "Intel" if "Intel" in raw else "Unknown"
        )
        mem = re.search(r"(\d+)\s*GB", raw, re.I)
        model = (
            raw.replace("NVIDIA", "").replace("AMD", "").replace("Intel", "").strip()
        )
        return f"""
        :{id} rdf:type :GPU ;
            :brand "{brand}" ;
            :model "{model}" ;
            :memory "{mem.group(1) if mem else '?'}"^^xsd:integer .
        """

    @staticmethod
    def storage_entity(id: str, raw: str) -> str:
        cap = re.search(r"(\d+)\s*TB", raw, re.I) or re.search(r"(\d+)\s*GB", raw, re.I)
        typ = (
            "SSD"
            if "SSD" in raw.upper()
            else "HDD" if "HDD" in raw.upper() else "Unknown"
        )
        iface = (
            "PCIe NVMe M.2" if "NVMe" in raw else "SATA" if "SATA" in raw else "Unknown"
        )
        return f"""
        :{id} rdf:type :Storage ;
            :capacity "{cap.group(1) if cap else '?'}" ;
            :type "{typ}" ;
            :interface "{iface}" .
        """

    @staticmethod
    def resolution_entity(id: str, raw: str) -> str:
        res = re.search(r"(\d{3,4})\s*[x×]\s*(\d{3,4})", raw)
        return f"""
        :{id} rdf:type :Display ;
            :resolution "{res.group(1)}x{res.group(2)}" ;
        """

    @staticmethod
    def brightness_entity(id: str, raw: str) -> str:
        bright = re.search(r"(\d+)\s*nits", raw, re.I)
        return f"""
        :{id} rdf:type :Display ;
            :brightness "{bright.group(1) if bright else '?'} nits" ;
        """

    @staticmethod
    def refresh_rate_entity(id: str, raw: str) -> str:
        refresh = re.search(r"(\d+)\s*Hz", raw, re.I)
        return f"""
        :{id} rdf:type :Display ;
            :refreshRate "{refresh.group(1)+'Hz' if refresh else '?'}" ;
        """

    @staticmethod
    def screen_size_entity(id: str, raw: str) -> str:
        size = re.search(r"(\d{2}\.?\d*)[″\"]", raw)
        return f"""
        :{id} rdf:type :Display ;
            :screenSize "{size.group(1)+'inch' if size else '?'}" .
        """

    @staticmethod
    def battery_entity(id: str, raw: str) -> str:
        cap = re.search(r"(\d+)\s*wh", raw, re.I)
        return f"""
        :{id} rdf:type :Battery ;
            :capacity "{cap.group(1) if cap else '?'}Wh" .
        """

    @staticmethod
    def weight_entity(id: str, raw: str) -> str:
        kg = re.search(r"([\d\.]+)\s*kg", raw, re.I)
        return f"""
        :{id} rdf:type :Weight ;
            :value "{kg.group(1) if kg else '?'}"^^xsd:decimal ;
            :unit "kg" .
        """


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


def parse_specifications(product, other_entities):
    """Convert specifications to OWL format specifications"""
    owl_specs = []
    specs = product.get("specifications", {})

    # Map specifications to OWL format
    if specs.get("brand"):
        owl_specs.append(f":{clean_string(specs['brand'])}")

    if specs.get("CPU"):
        owl_specs.append(f":{CPU_MAP[specs['CPU']]}")
        _tmp = ParseOtherEntitiesJSONToOWL.cpu_entity(
            CPU_MAP[specs["CPU"]], specs["CPU"]
        )
        other_entities[CPU_MAP[specs["CPU"]]] = _tmp

    if specs.get("Ram"):
        owl_specs.append(f":{RAM_MAP[specs['Ram']]}")
        _tmp = ParseOtherEntitiesJSONToOWL.ram_entity(
            RAM_MAP[specs["Ram"]], specs["Ram"]
        )
        other_entities[RAM_MAP[specs["Ram"]]] = _tmp

    _storage_key = specs.get("Ổ cứng", None) or specs.get("Storage", None)
    if _storage_key:
        owl_specs.append(f":{STORAGE_MAP[_storage_key]}")
        _tmp = ParseOtherEntitiesJSONToOWL.storage_entity(
            STORAGE_MAP[_storage_key], _storage_key
        )
        other_entities[STORAGE_MAP[_storage_key]] = _tmp

    _gpu_key = specs.get("Card màn hình", None) or specs.get("Graphics card", None)
    if _gpu_key:
        owl_specs.append(f":{GPU_MAP[_gpu_key]}")
        _tmp = ParseOtherEntitiesJSONToOWL.gpu_entity(GPU_MAP[_gpu_key], _gpu_key)
        other_entities[GPU_MAP[_gpu_key]] = _tmp

    try:
        if specs.get("Độ phân giải") or specs.get("Resolution"):
            _resolution_key = AggregateData.get_resolution_subinfo(
                product, ResolutionSubInfo.RESOLUTION.value
            )
            if _resolution_key:
                _resolution = RESOLUTION_MAP[_resolution_key]
                owl_specs.append(":" + _resolution)
                _tmp = ParseOtherEntitiesJSONToOWL.resolution_entity(
                    _resolution, specs.get("Độ phân giải") or specs.get("Resolution")
                )
                other_entities[
                    RESOLUTION_MAP[specs.get("Độ phân giải") or specs.get("Resolution")]
                ] = _tmp

            _brightness_key = AggregateData.get_resolution_subinfo(
                product, ResolutionSubInfo.BRIGHTNESS.value, 1
            )
            if _brightness_key:
                _brightness = BRIGHTNESS_MAP[_brightness_key]
                owl_specs.append(":" + _brightness)
                _tmp = ParseOtherEntitiesJSONToOWL.brightness_entity(
                    _resolution, specs.get("Độ phân giải") or specs.get("Resolution")
                )
                other_entities[
                    BRIGHTNESS_MAP[specs.get("Độ phân giải") or specs.get("Resolution")]
                ] = _tmp

            _refresh_rate_key = AggregateData.get_resolution_subinfo(
                product, ResolutionSubInfo.REFRESH_RATE.value, 1
            )
            if _refresh_rate_key:
                _refresh_rate = REFRESH_RATE_MAP[_refresh_rate_key]
                owl_specs.append(":" + _refresh_rate)
                _tmp = ParseOtherEntitiesJSONToOWL.refresh_rate_entity(
                    _resolution, specs.get("Độ phân giải") or specs.get("Resolution")
                )
                other_entities[
                    REFRESH_RATE_MAP[
                        specs.get("Độ phân giải") or specs.get("Resolution")
                    ]
                ] = _tmp

            _screen_size_key = AggregateData.get_resolution_subinfo(
                product, ResolutionSubInfo.SCREEN_SIZE.value, 1
            )
            if _screen_size_key:
                _screen_size = SCREEN_MAP[_screen_size_key]
                owl_specs.append(":" + _screen_size)
                _tmp = ParseOtherEntitiesJSONToOWL.screen_size_entity(
                    _resolution, specs.get("Độ phân giải") or specs.get("Resolution")
                )
                other_entities[
                    SCREEN_MAP[specs.get("Độ phân giải") or specs.get("Resolution")]
                ] = _tmp

    except Exception as e:
        print(
            f"Error processing resolution for product {product.get('title', '')}: {e}"
        )

    _battery_key = specs.get("Pin", None) or specs.get("Battery", None)
    if _battery_key:
        _battery_key = _battery_key.lower()
        if _battery_key.endswith("w"):
            _battery_key += "h"
        owl_specs.append(f":{BATTERIES_MAP[_battery_key]}")
        _tmp = ParseOtherEntitiesJSONToOWL.battery_entity(
            BATTERIES_MAP[_battery_key], _battery_key
        )
        other_entities[BATTERIES_MAP[_battery_key]] = _tmp

    _weight_key = specs.get("Trọng lượng", None) or specs.get("Weight", None)
    if _weight_key:
        owl_specs.append(f":{WEIGHT_MAP[_weight_key]}")
        _tmp = ParseOtherEntitiesJSONToOWL.weight_entity(
            WEIGHT_MAP[_weight_key], _weight_key
        )
        other_entities[WEIGHT_MAP[_weight_key]] = _tmp

    return owl_specs, other_entities


def json_to_owl(json_data):
    """Transform JSON data to OWL format"""
    owl_content = []
    other_entities = {}

    for item in json_data:
        # Create product identifier from title
        product_id = clean_string(item["title"])

        # Start product definition
        owl_content.append(f":{product_id} rdf:type :Product ;")

        # Add specifications
        specs, other_entities = parse_specifications(item, other_entities)
        if specs:
            owl_content.append(
                "    :hasSpecification "
                + " ,\n                      ".join(specs)
                + " ;"
            )

        # Add price
        price = extract_price(item["price"])
        owl_content.append(f'    :hasPrice "{price}"^^xsd:decimal ;')

        img_url = item["image_url"]
        owl_content.append(f'    :hasImage "{img_url}".')

        owl_content.append("")  # Empty line between products

    other_entities_list = list(other_entities.values())
    if other_entities_list:
        owl_content.append("\n".join(other_entities_list))
    return "\n".join(owl_content)


def transform():
    # Read JSON file
    with open(
        "./data_process/scrape/sazo_laptops_enriched.json", "r", encoding="utf-8"
    ) as file:
        json_data = json.load(file)

    # Transform to OWL
    owl_output = json_to_owl(json_data)

    # Write output to file
    with open(
        "./data_process/process/owl_outputs/output_2.owl", "w", encoding="utf-8"
    ) as file:
        file.write(owl_output)


if __name__ == "__main__":
    # Agrregate data/Analyze data
    # AggregateData.execute()

    transform()
