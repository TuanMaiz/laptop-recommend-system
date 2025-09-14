import re
import json

# --- Full purpose map (simplified: add all yours here) ---
with open(
    "./data_process/process/sub_process/unique_key.json", "r", encoding="utf-8"
) as f:
    purpose_map = json.load(f)


class SpecClassifier:
    @staticmethod
    def classify_spec(name):
        """Return purpose for a spec by name."""
        for category, groups in purpose_map.items():
            for comp_type, items in groups.items():
                if name in items:
                    return category
        return None

    @staticmethod
    def process_specs(input_file, output_file):
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by spec blocks (start with :)
        specs = re.split(r"(?=\n:)", content)

        updated_specs = []
        for spec in specs:
            match = re.match(r":(\S+)\s+rdf:type\s+:(\S+)", spec.strip())
            if not match:
                updated_specs.append(spec)
                continue

            name, spec_type = match.groups()
            category = SpecClassifier.classify_spec(name)

            if category:
                # Attach satisfiesRequirement
                spec = (
                    spec.strip().rstrip(".")
                    + f" ;\n    :satisfiesRequirement :{category} .\n"
                )

            updated_specs.append(spec)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(updated_specs))

        print(f"✅ Updated specifications saved to {output_file}")


def classify(cpu, ram, gpu):
    """Return one category: Gaming > Graphic > Office"""
    print(cpu)
    if (
        cpu in purpose_map["Gaming"]["CPU"]
        and gpu in purpose_map["Gaming"]["GPU"]
        and ram in purpose_map["Gaming"]["RAM"]
    ) or (cpu in purpose_map["Gaming"]["CPU"] and gpu in purpose_map["Gaming"]["GPU"]):
        return "Gaming"
    if (
        (cpu in purpose_map["Gaming"]["CPU"] or cpu in purpose_map["Graphic"]["CPU"])
        and gpu in purpose_map["Graphic"]["GPU"]
        and ram in purpose_map["Graphic"]["RAM"]
    ) or (
        (cpu in purpose_map["Gaming"]["CPU"] or cpu in purpose_map["Graphic"]["CPU"])
        and gpu in purpose_map["Graphic"]["GPU"]
    ):
        return "Graphic"
    return "Office"


def process_owl(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split products
    products = re.split(r"(?=\n:)", content)

    updated_products = []
    for product in products:
        if ":Product" not in product:
            updated_products.append(product)
            continue

        # Extract specs
        block_match = re.search(r":hasSpecification\s+([^;]+);", product, re.DOTALL)
        specs = []
        if block_match:
            block_content = block_match.group(1)
            # Extract all specs like :cpu_xxx, :ram_xxx, etc.
            specs = re.findall(r":(\S+)", block_content)
        cpu = next((s for s in specs if s.startswith("cpu_")), None)
        ram = next((s for s in specs if s.startswith("ram_")), None)
        gpu = next((s for s in specs if s.startswith("gpu_")), None)

        if cpu and ram and gpu:
            category = classify(cpu, ram, gpu)
            # Add satisfiesRequirement triple
            product = (
                product.strip().rstrip(".")
                + f" ;\n    :satisfiesRequirement :{category} .\n"
            )

        updated_products.append(product)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_products))

    print(f"✅ Updated OWL saved to {output_file}")


# Example usage
# process_owl(
#     "./data_process/process/owl_outputs/output_2_.owl",
#     "./data_process/process/owl_outputs/laptops_classified.owl",
# )


SpecClassifier.process_specs(
    "./data_process/process/owl_outputs/output_2_.owl",
    "./data_process/process/owl_outputs/specs_classified.owl",
)
