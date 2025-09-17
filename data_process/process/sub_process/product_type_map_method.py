import re

# --- classification dictionary from before ---
components_tier = {
    "CPU": {
        "HighEnd": ["cpu_amd_ryzen_9_8940hx","cpu_amd_ryzen_9_8945hx","cpu_intel_core_i9_14900hx",
                    "cpu_intel_core_i9_13900hx","cpu_intel_core_ultra_9_275hx","cpu_intel_core_ultra_9_285h",
                    "cpu_intel_core_ultra_9_processor_185h","cpu_amd_ryzen_ai_9_pro_375","cpu_amd_ryzen_ai_9_hx_pro_375",
                    "cpu_intel_core_ultra_9_275h"],
        "MiddleEnd": ["cpu_amd_ryzen_7_8845hx","cpu_amd_ryzen_7_h255","cpu_amd_ryzen_7_h260",
                      "cpu_amd_ryzen_7_8745hs","cpu_intel_core_i7_14700hx","cpu_intel_core_i7_14650hx",
                      "cpu_intel_core_i7_13650hx","cpu_intel_core_i7_1360p","cpu_intel_core_ultra_7_255hx",
                      "cpu_intel_core_ultra_7_255h","cpu_intel_core_ultra_7_155u","cpu_intel_core_ultra_7_processor_155h"],
        "LowEnd": ["cpu_amd_ryzen_5_8545h","cpu_intel_core_i5_1240p","cpu_intel_core_i5_1340p",
                   "cpu_intel_core_i5_13450hx","cpu_intel_core_i5_14500hx","cpu_intel_core_ultra_5_125u",
                   "cpu_intel_core_ultra_5_225h","cpu_intel_core_ultra_5_processor_125h"]
    },
    "RAM": {
        "HighEnd": ["ram_64gb_ddr5_5600_up","ram_64gb_ddr5_5600_dual_up","ram_64gb_lpddr5x_7500_nonup",
                    "ram_64gb_lpddr5x_8400_nonup"],
        "MiddleEnd": ["ram_32gb_ddr5_4800_up","ram_32gb_ddr5_5600_up","ram_32gb_ddr5_6400_up",
                      "ram_32gb_ddr5_5600_dual_up","ram_32gb_lpddr5x_nonup","ram_32gb_lpddr5x_7467_nonup",
                      "ram_32gb_lpddr5x_7500_nonup","ram_32gb_lpddr5x_8400_nonup"],
        "LowEnd": ["ram_8gb_lpddr5_4800_nonup","ram_16gb_lpddr5x_8400_nonup","ram_16gb_ddr4_3200_up",
                   "ram_16gb_ddr5_4800_up","ram_16gb_ddr5_5200_up","ram_16gb_ddr5_5600_up",
                   "ram_16gb_lpddr5x_nonup","ram_16gb_lpddr5_4800_nonup","ram_24gb_ddr5_4800_up"]
    },
    "GPU": {
        "HighEnd": ["gpu_nvidia_rtx_5070ti_12gb","gpu_nvidia_rtx_5080_16gb","gpu_combo_intel_arc_140t_nvidia_rtx_5000_12gb"],
        "MiddleEnd": ["gpu_nvidia_rtx_4070_8gb","gpu_nvidia_rtx_4060_8gb","gpu_nvidia_rtx_4050_6gb",
                      "gpu_nvidia_rtx_5050_6gb","gpu_nvidia_rtx_5060_8gb","gpu_nvidia_rtx_5070_8gb",
                      "gpu_combo_intel_arc_140t_nvidia_rtx_5060_8gb","gpu_combo_intel_arc_140t_nvidia_rtx_5050_6gb",
                      "gpu_combo_intel_arc_integrated_nvidia_rtx_5060_8gb","gpu_combo_intel_integrated_nvidia_rtx_5060_8gb",
                      "gpu_combo_intel_integrated_nvidia_rtx_5070_8gb"],
        "LowEnd": ["gpu_intel_iris_xe","gpu_intel_arc_integrated","gpu_intel_arc_130t","gpu_intel_arc_140t",
                   "gpu_intel_arc_185t","gpu_amd_radeon_integrated","gpu_amd_radeon_780m","gpu_amd_radeon_860m",
                   "gpu_amd_radeon_890m","gpu_intel_integrated"]
    },
    "Storage": {
        "HighEnd": ["storage_2tb_pcie4_nvme_m2","storage_2tb_pcie4_nvme_m2_dual","storage_2tb_pcie4_nvme_dual"],
        "MiddleEnd": ["storage_1tb_pcie4_nvme_m2","storage_1tb_pcie4_nvme_tlc_m2","storage_1tb_pcie4_ssd",
                      "storage_1tb_pcie_nvme_m2","storage_1tb_pcie_nvme_m2_dual","storage_1tb_pcie4_nvme_2242_m2"],
        "LowEnd": ["storage_512gb_pcie_nvme_m2","storage_512gb_pcie4_nvme_m2","storage_512gb_pcie_nvme_m2_dual",
                   "storage_512gb_pcie4_nvme_m2_dual"]
    },
    "Resolution": {
        "HighEnd": ["resolution_3840x2400","resolution_3200x2000","resolution_3072x1920","resolution_2880x1920"],
        "MiddleEnd": ["resolution_2880x1800","resolution_2880x1620","resolution_2560x1600","resolution_2560x1440","resolution_2240x1400"],
        "LowEnd": ["resolution_1920x1080","resolution_1920x1200"]
    },
    "Battery": {
        "HighEnd": ["battery_300WH","battery_330WH","battery_400WH","battery_280WH"],
        "MiddleEnd": ["battery_90WH","battery_86WH","battery_85WH","battery_80WH","battery_75WH"],
        "LowEnd": ["battery_57WH","battery_60WH","battery_65WH","battery_70WH","battery_55WH"]
    }
}

# Reverse lookup for quick classification
reverse_map = {}
for comp_type, tiers in components_tier.items():
    for tier, ids in tiers.items():
        for cid in ids:
            reverse_map[cid] = tier

def classify_laptop(components):
    scores = {"HighEnd": 0, "MiddleEnd": 0, "LowEnd": 0}
    for comp in components:
        if comp in reverse_map:
            scores[reverse_map[comp]] += 1
    # Decision logic
    if scores["HighEnd"] >= 2:
        return "HighEnd"
    elif scores["LowEnd"] >= 2:
        return "LowEnd"
    else:
        return "MiddleEnd"

# --- Read file and classify ---
with open("./laptops_rtf.txt", "r", encoding="utf-8") as f:
    data = f.read()

def rewrite_blocks(products):
    output = []
    for block, tier in products:
        # replace "rdf:type :Product" with rdf:type :HighEnd / :MiddleEnd / :LowEnd
        new_block = re.sub(r"rdf:type\s+:Product", f"rdf:type :{tier}", block)
        output.append(new_block)
    return "\n\n".join(output)

results = []
products = re.split(r"(?=\n:)", data)
for product in products:
    product = product.strip()
    block_match = re.search(r":hasSpecification\s+([^;]+);", product, re.DOTALL)
    specs = []
    if block_match:
        block_content = block_match.group(1)
        # Extract all specs like :cpu_xxx, :ram_xxx, etc.
        specs = re.findall(r":(\S+)", block_content)

    name_match = re.search(r"^:(\w+)", product.strip())
    if not name_match:
        continue
    name = name_match.group(1)
    # print(f"{name}: {specs}...")

    # # # components = re.findall(r":(\S+)", specs)
    tier = classify_laptop(specs)
    # print(f"{name}: {tier}")
    results.append((product, tier))


# for product, tier in results.items():
#     print(f":{product} rdf:type :{tier} .")

final_output = rewrite_blocks(results)
with open("./output_final.owl", "w", encoding="utf-8") as f:
    f.write(final_output)