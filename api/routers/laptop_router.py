import os
from typing import List, Optional, Any
from fastapi import APIRouter, HTTPException, Query, Header
from fastapi.params import Depends
import psycopg2
from sqlalchemy.orm import Session
from api.db.session import SessionLocal
from api.schemas.laptop_schema import LaptopBase
from api.db.models.laptop_model import Laptop
from api.schemas.fingerprint_schema import FingerprintCheckRequest, FirstTimeReference
from api.services.recommendation_service import RecommendationService
from api.services.laptop_service import LaptopService
from pydantic import BaseModel, ConfigDict
from fastapi import status

router = APIRouter(prefix="/laptops")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_laptops(limit: int = 20):
    service = LaptopService()
    laptops = service.list_laptop()

    laptop_list = []
    for laptop in laptops[:limit]:
        laptop_data = laptop["properties"]
        # Extract friendly name from URI
        friendly_name = laptop["name"]

        # Parse specifications into human-readable format
        print(50 * "=")
        print(laptop_data.items())
        print(50 * "=")

        # Get specifications from laptop object
        specifications = laptop.get("specifications", [])
        parsed_specs = {}

        # Process basic properties
        for prop_uri, prop_value in laptop_data.items():
            prop_name = prop_uri.split("#")[-1]
            if "price" in prop_name.lower():
                parsed_specs["price"] = prop_value
            elif "image" in prop_name.lower():
                parsed_specs["image"] = prop_value
            elif "satisfiesRequirement" in prop_name.lower():
                parsed_specs["requirement"] = (
                    prop_value.split("#")[-1] if "#" in prop_value else prop_value
                )

        # Process detailed specifications
        for spec in specifications:
            spec_name = spec["name"]
            spec_type = spec["type"]

            # Extract readable spec name
            readable_name = (
                spec_name.replace("_", " ")
                .replace("gb", "GB")
                .replace("tb", "TB")
                .replace("ssd", "SSD")
            )

            # Extract spec properties
            for prop_name, prop_value in spec["properties"].items():
                if prop_name.lower() == "name":
                    parsed_specs[spec_type.lower()] = f"{readable_name}"
                elif prop_name.lower() == "value":
                    if spec_type.lower() in parsed_specs:
                        parsed_specs[spec_type.lower()] += f" {prop_value}"
                    else:
                        parsed_specs[spec_type.lower()] = prop_value
                else:
                    prop_display_name = prop_name.replace("_", " ").lower()
                    parsed_specs[prop_display_name] = prop_value

        laptop_list.append(
            {"id": laptop["uri"], "name": friendly_name, "specifications": parsed_specs}
        )

    return {"laptops": laptop_list}

    # laptops = db.query(Laptop).limit(limit).all()
    # if not laptops:
    #     raise HTTPException(status_code=404, detail="No laptops found")
    # return laptops


@router.get("/{id}", response_model=LaptopBase)
def get_laptop_detail(id: str, db: Session = Depends(get_db)):
    laptop = db.query(Laptop).filter(Laptop.id == id).first()
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop


class DeviceInfo(BaseModel):
    isMobile: bool
    isTablet: bool
    isDesktop: bool
    browser: str
    os: str


class BaseEventModel(BaseModel):
    id: str
    timestamp: str
    pageUrl: str
    userId: Optional[str] = None
    sessionId: Optional[str] = None
    fingerprint: Optional[str] = None
    eventType: str
    eventData: Optional[Any] = None
    deviceInfo: Optional[Any] = None
    ipAddress: Optional[str] = None
    priority: Optional[str] = None
    userAgent: Optional[str] = None


@router.post("/is-first-time", status_code=status.HTTP_201_CREATED)
def track_interaction_first_time(
    fingerprint: FingerprintCheckRequest, db: Session = Depends(get_db)
):

    # get cors on front end
    print(fingerprint)

    return {"message": "success", "data": {"firstTime": True}}

    # not get cors
    # print(fingerprint)

    # return {"status": "interaction recorded" }


@router.post("/track-interaction-first-time", status_code=status.HTTP_201_CREATED)
def track_interaction_first_time(
    events: List[BaseEventModel], db: Session = Depends(get_db)
):
    return {"status": "interaction recorded"}
