from .collab_filtering_service import RDFUSM as USM
import os

from pathlib import Path

root_dir = Path(__file__).resolve().parents[3]
owl_file_path = os.path.join(root_dir, "laptops.owl")

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
    "ThinkBook_14P_AI_2025_Ultra_9275H_32GB_RAM_1TB_SSD",
    2,
)


{
    "success": true,
    "payload": [
        {
            "product_uri": "http://example.org/laptop#HP_Elitebook_6_G1a_14_2025_Ryzen_7_H_255_32GB_RAM_1TB_SSD",
            "model": "HP_Elitebook_6_G1a_14_2025_Ryzen_7_H_255_32GB_RAM_1TB_SSD",
            "price": 21600000,
            "image": "https://sazo.vn/storage/products/hp-6-g1i-14/1-1.png",
            "specs": {},
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.235294117647059,
        },
        {
            "product_uri": "http://example.org/laptop#Thinkbook_16_G7_2025_R7_H_260_32GB_RAM_1TB_SSD",
            "model": "Thinkbook_16_G7_2025_R7_H_260_32GB_RAM_1TB_SSD",
            "price": 21390000,
            "image": "https://sazo.vn/storage/products/16g7-ai7/1-1.png",
            "specs": {},
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.153846153846153,
        },
        {
            "product_uri": "http://example.org/laptop#HP_Spectre_x360_14_2025_Ultra_7155H_32GB_RAM_1TB_SSD",
            "model": "HP_Spectre_x360_14_2025_Ultra_7155H_32GB_RAM_1TB_SSD",
            "price": 34900000,
            "image": "https://sazo.vn/storage/products/spectre-x360-14/1-1.png",
            "specs": {},
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.153846153846153,
        },
        {
            "product_uri": "http://example.org/laptop#HP_Spectre_x360_14_2025_Ultra_9185H_32GB_RAM_1TB_SSD",
            "model": "HP_Spectre_x360_14_2025_Ultra_9185H_32GB_RAM_1TB_SSD",
            "price": 39500000,
            "image": "https://sazo.vn/storage/products/spectre-x360-14/1-1.png",
            "specs": {},
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.153846153846153,
        },
        {
            "product_uri": "http://example.org/laptop#Thinkbook_14_G7_2025_R7_H_260_32GB_RAM_1TB_SSD",
            "model": "Thinkbook_14_G7_2025_R7_H_260_32GB_RAM_1TB_SSD",
            "price": 20790000,
            "image": "https://sazo.vn/storage/products/14g7-ai7/1-1.png",
            "specs": {},
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.153846153846153,
        },
    ],
    "code": 200,
}


{
    "success": true,
    "payload": [
        {
            "product_uri": "http://example.org/laptop#ThinkPad_T14P_AI_2025_Ultra_7255H_32GB_RAM_1TB_SSD",
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 5,
        },
        {
            "product_uri": "http://example.org/laptop#HP_Elitebook_6_G1a_14_2025_Ryzen_7_H_255_32GB_RAM_1TB_SSD",
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.35,
        },
        {
            "product_uri": "http://example.org/laptop#Thinkbook_14_G7_2025_R7_H_260_32GB_RAM_1TB_SSD",
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.3125,
        },
        {
            "product_uri": "http://example.org/laptop#HP_Spectre_x360_14_2025_Ultra_7155H_32GB_RAM_1TB_SSD",
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.3125,
        },
        {
            "product_uri": "http://example.org/laptop#Thinkbook_16_G7_2025_R7_H_260_32GB_RAM_1TB_SSD",
            "satisreq": "Graphic",
            "range": "MiddleEnd",
            "cf_score": 4.3125,
        },
    ],
    "code": 200,
}
