from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Laptop(BaseModel):
    id: int
    title: str
    url: str
    price: float
    brand: str
    weight_kg: Optional[float]
    cpu_id: str
    ram_id: str
    storage_id: str
    screen_id: str
    description: Optional[str]
    image_url: Optional[str]
    scraped_at: datetime  # Use datetime if you want: datetime


class CPU(BaseModel):
    id: str
    cpu_model: str
    core_count: int
    thread_count: int
    base_clock_ghz: Optional[float]
    boost_clock_ghz: Optional[float]
    cache_mb: Optional[float]
    brand: str


class RAM(BaseModel):
    id: str
    ram_size_gb: int
    ram_type: Optional[str]
    upgradeable: Optional[bool]
    speed_mhz: Optional[int]


class Storage(BaseModel):
    id: str
    storage_size_gb: int
    storage_type: Optional[str]
    interface: Optional[str]


class Screen(BaseModel):
    id: str
    size_inch: Optional[float]
    resolution: Optional[str]
    panel_type: Optional[str]
    refresh_rate_hz: Optional[int]
    brightness_nits: Optional[int]
    color_gamut: Optional[str]
    touch: Optional[bool]


class GPU(BaseModel):
    id: str
    gpu_model: str
    vram_gb: Optional[int]
    is_dedicated: Optional[bool]
