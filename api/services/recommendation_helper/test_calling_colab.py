from .collab_filtering_service import RDFUSM as USM
import os

from pathlib import Path

root_dir = Path(__file__).resolve().parents[2]
owl_file_path = os.path.join(
    "/Users/khoaiquin/Storage/Cơ sở trí thức/laptop-recommend-system", "laptops.owl"
)
usm = USM(owl_file_path)

# Init from frontend input
# usm.init_profile(
#     fingerprint="abc123",
#     functionality="Gaming",
#     specs=["cpu_intel_core_ultra_9_275hx", "ram_32gb_ddr5_6400_up"],
#     price="HighEnd",
# )

# # Add rating
usm.rate_product(
    "User_abc123",
    "Xiaoxin_Pro_16c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
    2,
)

# Recommend
# print(usm.recommend("abc123"))

# [
#     {
#         "product_uri": "http://example.org/laptop#Xiaoxin_Pro_16c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
#         "model": "Xiaoxin_Pro_16c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
#         "cf_score": 5.0,
#     },
#     {
#         "product_uri": "http://example.org/laptop#ThinkPad_P16s_2025_Ryzen_Pro_R9_H_375_32GB_RAM_1TB_SSD",
#         "model": "ThinkPad_P16s_2025_Ryzen_Pro_R9_H_375_32GB_RAM_1TB_SSD",
#         "cf_score": 4.624999999999999,
#     },
#     {
#         "product_uri": "http://example.org/laptop#HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_32GB_RAM_1TB_SSD",
#         "model": "HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_32GB_RAM_1TB_SSD",
#         "cf_score": 4.624999999999999,
#     },
#     {
#         "product_uri": "http://example.org/laptop#ThinkPad_T16_Gen_3_2025_AI_7_350_32GB_RAM_1TB_SSD",
#         "model": "ThinkPad_T16_Gen_3_2025_AI_7_350_32GB_RAM_1TB_SSD",
#         "cf_score": 4.624999999999999,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Legion_5_2025_Y7000P_I914900HX_16GB_RAM_1TB_SSD_RTX_50605070",
#         "model": "Legion_5_2025_Y7000P_I914900HX_16GB_RAM_1TB_SSD_RTX_50605070",
#         "cf_score": 4.624999999999999,
#     },
#     {
#         "product_uri": "http://example.org/laptop#ThinkPad_T14_Gen_6_2025_AI_7_350_32GB_RAM_1TB_SSD",
#         "model": "ThinkPad_T14_Gen_6_2025_AI_7_350_32GB_RAM_1TB_SSD",
#         "cf_score": 4.624999999999999,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Xiaoxin_Pro_14c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
#         "model": "Xiaoxin_Pro_14c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
#         "cf_score": 4.583333333333333,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_32GB_RAM_1TB_SSD",
#         "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_32GB_RAM_1TB_SSD",
#         "cf_score": 4.583333333333333,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_16GB_RAM_512GB_SSD",
#         "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_16GB_RAM_512GB_SSD",
#         "cf_score": 4.583333333333333,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_5420_i5_1240P_16GB_RAM_512GB_SSD",
#         "model": "Dell_Inspiron_5420_i5_1240P_16GB_RAM_512GB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_64GB_RAM_1TB_SSD_DreamColor",
#         "model": "HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_64GB_RAM_1TB_SSD_DreamColor",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_G15_5530_i5_13450HX_16GB_RAM_512GB_SSD_RTX_4050",
#         "model": "Dell_G15_5530_i5_13450HX_16GB_RAM_512GB_SSD_RTX_4050",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_1TB_SSD",
#         "model": "Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_1TB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_i7_1360P_16GB_RAM_512GB_SSD",
#         "model": "Dell_Inspiron_16_5630_i7_1360P_16GB_RAM_512GB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_i5_1340P_8GB_RAM_512GB_SSD",
#         "model": "Dell_Inspiron_16_5630_i5_1340P_8GB_RAM_512GB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_5420_i51240P_16GB_RAM_512GB_SSD",
#         "model": "Dell_Inspiron_5420_i51240P_16GB_RAM_512GB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_Ultra_7155U_16GB_RAM_1TB_SSD",
#         "model": "Dell_Inspiron_16_5630_Ultra_7155U_16GB_RAM_1TB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_64GB_RAM_2TB_SSD",
#         "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_64GB_RAM_2TB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_32GB_RAM_1TB_SSD",
#         "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_32GB_RAM_1TB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_512GB_SSD",
#         "model": "Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_512GB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_Inspiron_14_5430_i7_1360P_16GB_RAM_512GB_SSD",
#         "model": "Dell_Inspiron_14_5430_i7_1360P_16GB_RAM_512GB_SSD",
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_XPS_16_9635_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
#         "model": "Dell_XPS_16_9635_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
#         "cf_score": 4.375,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Dell_XPS_14_9440_Touch_OLED_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
#         "model": "Dell_XPS_14_9440_Touch_OLED_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
#         "cf_score": 4.375,
#     },
#     {
#         "product_uri": "http://example.org/laptop#ThinkBook_14P_AI_2025_Ultra_9275H_32GB_RAM_1TB_SSD",
#         "model": "ThinkBook_14P_AI_2025_Ultra_9275H_32GB_RAM_1TB_SSD",
#         "cf_score": 4.0,
#     },
# ]

# [
#     {
#         "product_uri": "http://example.org/laptop#Legion_Pro_7i_2025_Y9000P_BlackUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070Ti",
#         "model": "Legion_Pro_7i_2025_Y9000P_BlackUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070Ti",
#         "price": 67290000.0,
#         "image": "https://sazo.vn/storage/products/y9000p-2025/1-1-1.png",
#         "specs": {
#             "Battery": {"capacity": "80Wh"},
#             "CPU": {
#                 "baseClock": "2.1GHz",
#                 "boostClock": "5.4GHz",
#                 "brand": "Intel",
#                 "cache": "36MB",
#                 "cores": 24,
#                 "model": "Core Ultra 9 275HX  24 luồng, xung nhịp cơ bản từ 2.1GHz có thể đạt max với turbo boost lên tới 5.4GHz, 36MB Cache)",
#                 "threads": 24,
#             },
#             "GPU": {
#                 "brand": "NVIDIA",
#                 "model": "® Graphics + ® GeForce RTX 5070Ti Laptop GPU 12GB GDDR7",
#                 "vramMemory": 12,
#             },
#             "RAM": {"memory": 32, "speed": "6400MHz", "upgradeable": False},
#             "Specification": {},
#             "Storage": {"capacity": "1", "interface": "Unknown"},
#             "Weight": {"unit": "kg", "value": Decimal("2.57")},
#         },
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Legion_Pro_7i_2025_Y9000P_WhiteUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070Ti",
#         "model": "Legion_Pro_7i_2025_Y9000P_WhiteUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070Ti",
#         "price": 67290000.0,
#         "image": "https://sazo.vn/storage/products/y9000p-2025/1-1-1.png",
#         "specs": {
#             "Battery": {"capacity": "80Wh"},
#             "CPU": {
#                 "baseClock": "2.1GHz",
#                 "boostClock": "5.4GHz",
#                 "brand": "Intel",
#                 "cache": "36MB",
#                 "cores": 24,
#                 "model": "Core Ultra 9 275HX  24 luồng, xung nhịp cơ bản từ 2.1GHz có thể đạt max với turbo boost lên tới 5.4GHz, 36MB Cache)",
#                 "threads": 24,
#             },
#             "GPU": {
#                 "brand": "NVIDIA",
#                 "model": "® Graphics + ® GeForce RTX 5070Ti Laptop GPU 12GB GDDR7",
#                 "vramMemory": 12,
#             },
#             "RAM": {"memory": 32, "speed": "6400MHz", "upgradeable": False},
#             "Specification": {},
#             "Storage": {"capacity": "1", "interface": "Unknown"},
#             "Weight": {"unit": "kg", "value": Decimal("2.57")},
#         },
#         "cf_score": 4.5,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Legion_7_2025_Y9000X_BlackUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070",
#         "model": "Legion_7_2025_Y9000X_BlackUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070",
#         "price": 56800000.0,
#         "image": "https://sazo.vn/storage/products/y9000x-2025/1-1.png",
#         "specs": {
#             "Battery": {"capacity": "84Wh"},
#             "CPU": {
#                 "baseClock": "2.1GHz",
#                 "boostClock": "5.4GHz",
#                 "brand": "Intel",
#                 "cache": "36MB",
#                 "cores": 24,
#                 "model": "Core Ultra 9 275HX  24 luồng, xung nhịp cơ bản từ 2.1GHz có thể đạt max với turbo boost lên tới 5.4GHz, 36MB Cache)",
#                 "threads": 24,
#             },
#             "GPU": {
#                 "brand": "NVIDIA",
#                 "model": "® Graphics + ® GeForce RTX 5070 Laptop GPU 8GB GDDR7",
#                 "vramMemory": 8,
#             },
#             "RAM": {"memory": 32, "speed": "6400MHz", "upgradeable": False},
#             "Specification": {},
#             "Storage": {"capacity": "1", "interface": "Unknown"},
#             "Weight": {"unit": "kg", "value": Decimal("1.98")},
#         },
#         "cf_score": 4.411764705882353,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Lecoo_Fighter_7000_2025_R98940HX_16GB_RAM_1TB_SSD_RTX_5060",
#         "model": "Lecoo_Fighter_7000_2025_R98940HX_16GB_RAM_1TB_SSD_RTX_5060",
#         "price": 27000000.0,
#         "image": "https://sazo.vn/storage/products/lecoo-fighter-7000-r9/1-1.png",
#         "specs": {
#             "Specification": {},
#             "Battery": {"capacity": "80Wh"},
#             "CPU": {
#                 "baseClock": "2.4GHz",
#                 "boostClock": "5.3GHz",
#                 "brand": "AMD",
#                 "cache": "64MB",
#                 "cores": 16,
#                 "model": "Ryzen 9 8940HX",
#                 "threads": 32,
#             },
#             "GPU": {
#                 "brand": "NVIDIA",
#                 "model": "® GeForce RTX™ 5060 Laptop GPU 8GB GDDR7",
#                 "vramMemory": 8,
#             },
#             "RAM": {"memory": 16, "speed": "5200MHz", "upgradeable": False},
#             "Storage": {"capacity": "1", "interface": "PCIe NVMe M.2"},
#             "Weight": {"unit": "kg", "value": Decimal("2.4")},
#         },
#         "cf_score": 4.411764705882353,
#     },
#     {
#         "product_uri": "http://example.org/laptop#Legion_Pro_7_2025_R78845HX_32GB_RAM_1TB_SSD_RTX_5060",
#         "model": "Legion_Pro_7_2025_R78845HX_32GB_RAM_1TB_SSD_RTX_5060",
#         "price": 39500000.0,
#         "image": "https://sazo.vn/storage/products/legion-pro-7-2025/1-1.png",
#         "specs": {
#             "Battery": {"capacity": "80Wh"},
#             "CPU": {
#                 "baseClock": "3.8GHz",
#                 "boostClock": "5.1GHz",
#                 "brand": "AMD",
#                 "cache": "16MB",
#                 "cores": 8,
#                 "model": "Ryzen 7 8845HX",
#                 "threads": 16,
#             },
#             "GPU": {
#                 "brand": "NVIDIA",
#                 "model": "Radeon™ 780M + ® GeForce RTX 5060 Laptop GPU 8GB GDDR7",
#                 "vramMemory": 8,
#             },
#             "RAM": {"memory": 32, "speed": "5600MHz", "upgradeable": False},
#             "Specification": {},
#             "Storage": {"capacity": "1", "interface": "Unknown"},
#             "Weight": {"unit": "kg", "value": Decimal("2.57")},
#         },
#         "cf_score": 4.411764705882353,
#     },
# ]
