from collab_filtering_service import RDFUSM as USM

usm = USM("./laptop.owl")

# Init from frontend input
# usm.init_profile(
#     fingerprint="abc123",
#     functionality="Gaming",
#     specs=["cpu_intel_core_ultra_9_275hx", "ram_32gb_ddr5_6400_up"],
#     price="HighEnd",
# )

# # Add rating
# usm.rate_product(
#     "abc123",
#     "Legion_Pro_7i_2025_Y9000P_WhiteUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070Ti",
#     5,
# )

# Recommend
print(usm.recommend("xyz456"))

[
    {
        "product_uri": "http://example.org/laptop#Legion_Pro_7i_2025_Y9000P_WhiteUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070Ti",
        "model": "Legion_Pro_7i_2025_Y9000P_WhiteUltra_9275HX_32GB_RAM_1TB_SSD_RTX_5070Ti",
        "cf_score": 0.0,
    },
    {
        "product_uri": "http://example.org/laptop#HP_OMEN_17_2025_i714700HX_16GB_RAM_512GB_SSD_RTX_5060",
        "model": "HP_OMEN_17_2025_i714700HX_16GB_RAM_512GB_SSD_RTX_5060",
        "cf_score": None,
    },
    {
        "product_uri": "http://example.org/laptop#HP_OMEN_17_2025_i914900HX_32GB_RAM_1TB_SSD_RTX_5060",
        "model": "HP_OMEN_17_2025_i914900HX_32GB_RAM_1TB_SSD_RTX_5060",
        "cf_score": None,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Alienware_M18_R2_2025_i914900HX_32GB_RAM_1TB_SSD_RTX_5060",
        "model": "Dell_Alienware_M18_R2_2025_i914900HX_32GB_RAM_1TB_SSD_RTX_5060",
        "cf_score": None,
    },
    {
        "product_uri": "http://example.org/laptop#HP_Pavilion_Gaming_15_2025_R58545H_16GB_RAM_1TB_SSD_RTX_5060",
        "model": "HP_Pavilion_Gaming_15_2025_R58545H_16GB_RAM_1TB_SSD_RTX_5060",
        "cf_score": None,
    },
]

[
    {
        "product_uri": "http://example.org/laptop#Xiaoxin_Pro_16c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
        "model": "Xiaoxin_Pro_16c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
        "cf_score": 5.0,
    },
    {
        "product_uri": "http://example.org/laptop#ThinkPad_P16s_2025_Ryzen_Pro_R9_H_375_32GB_RAM_1TB_SSD",
        "model": "ThinkPad_P16s_2025_Ryzen_Pro_R9_H_375_32GB_RAM_1TB_SSD",
        "cf_score": 4.624999999999999,
    },
    {
        "product_uri": "http://example.org/laptop#HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_32GB_RAM_1TB_SSD",
        "model": "HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_32GB_RAM_1TB_SSD",
        "cf_score": 4.624999999999999,
    },
    {
        "product_uri": "http://example.org/laptop#ThinkPad_T16_Gen_3_2025_AI_7_350_32GB_RAM_1TB_SSD",
        "model": "ThinkPad_T16_Gen_3_2025_AI_7_350_32GB_RAM_1TB_SSD",
        "cf_score": 4.624999999999999,
    },
    {
        "product_uri": "http://example.org/laptop#Legion_5_2025_Y7000P_I914900HX_16GB_RAM_1TB_SSD_RTX_50605070",
        "model": "Legion_5_2025_Y7000P_I914900HX_16GB_RAM_1TB_SSD_RTX_50605070",
        "cf_score": 4.624999999999999,
    },
    {
        "product_uri": "http://example.org/laptop#ThinkPad_T14_Gen_6_2025_AI_7_350_32GB_RAM_1TB_SSD",
        "model": "ThinkPad_T14_Gen_6_2025_AI_7_350_32GB_RAM_1TB_SSD",
        "cf_score": 4.624999999999999,
    },
    {
        "product_uri": "http://example.org/laptop#Xiaoxin_Pro_14c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
        "model": "Xiaoxin_Pro_14c_2025_AI_7_H_350_32GB_RAM_1TB_SSDLenovo_IdeaPad_Slim_5",
        "cf_score": 4.583333333333333,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_32GB_RAM_1TB_SSD",
        "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_32GB_RAM_1TB_SSD",
        "cf_score": 4.583333333333333,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_16GB_RAM_512GB_SSD",
        "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R7350_16GB_RAM_512GB_SSD",
        "cf_score": 4.583333333333333,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_5420_i5_1240P_16GB_RAM_512GB_SSD",
        "model": "Dell_Inspiron_5420_i5_1240P_16GB_RAM_512GB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_64GB_RAM_1TB_SSD_DreamColor",
        "model": "HP_ZBook_8_G1a_14_2025_AI_9_HX_PRO_375_64GB_RAM_1TB_SSD_DreamColor",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_G15_5530_i5_13450HX_16GB_RAM_512GB_SSD_RTX_4050",
        "model": "Dell_G15_5530_i5_13450HX_16GB_RAM_512GB_SSD_RTX_4050",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_1TB_SSD",
        "model": "Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_1TB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_i7_1360P_16GB_RAM_512GB_SSD",
        "model": "Dell_Inspiron_16_5630_i7_1360P_16GB_RAM_512GB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_i5_1340P_8GB_RAM_512GB_SSD",
        "model": "Dell_Inspiron_16_5630_i5_1340P_8GB_RAM_512GB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_5420_i51240P_16GB_RAM_512GB_SSD",
        "model": "Dell_Inspiron_5420_i51240P_16GB_RAM_512GB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_Ultra_7155U_16GB_RAM_1TB_SSD",
        "model": "Dell_Inspiron_16_5630_Ultra_7155U_16GB_RAM_1TB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_64GB_RAM_2TB_SSD",
        "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_64GB_RAM_2TB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_32GB_RAM_1TB_SSD",
        "model": "Dell_XPS_13_9335_Touch_OLED_Ryzen_Pro_R9375_32GB_RAM_1TB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_512GB_SSD",
        "model": "Dell_Inspiron_16_5630_Ultra_5125U_16GB_RAM_512GB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_Inspiron_14_5430_i7_1360P_16GB_RAM_512GB_SSD",
        "model": "Dell_Inspiron_14_5430_i7_1360P_16GB_RAM_512GB_SSD",
        "cf_score": 4.5,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_XPS_16_9635_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
        "model": "Dell_XPS_16_9635_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
        "cf_score": 4.375,
    },
    {
        "product_uri": "http://example.org/laptop#Dell_XPS_14_9440_Touch_OLED_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
        "model": "Dell_XPS_14_9440_Touch_OLED_Ultra_9275H_64GB_RAM_2TB_SSD_RTX_5060",
        "cf_score": 4.375,
    },
    {
        "product_uri": "http://example.org/laptop#ThinkBook_14P_AI_2025_Ultra_9275H_32GB_RAM_1TB_SSD",
        "model": "ThinkBook_14P_AI_2025_Ultra_9275H_32GB_RAM_1TB_SSD",
        "cf_score": 4.0,
    },
]
