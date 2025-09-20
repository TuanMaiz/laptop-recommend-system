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
    laptop_uris = service.list_laptop()
    
    laptop_list = []
    for uri in laptop_uris[:limit]:
        laptop_data = service.get_laptop(uri)
        # Extract friendly name from URI
        friendly_name = uri.split("#")[-1].replace("_", " ")
        
        # Parse specifications into human-readable format
        print(50*"=")
        print(laptop_data.items())
        print(50*"=")
        parsed_specs = {}
        for spec_uri, spec_value in laptop_data.items():
            spec_name = spec_uri.split("#")[-1]
            if "price" in spec_name.lower():
                parsed_specs["price"] = spec_value
            elif "cpu" in spec_name.lower():
                parsed_specs["cpu"] = spec_value
            elif "ram" in spec_name.lower():
                parsed_specs["ram"] = spec_value
            elif "storage" in spec_name.lower():
                parsed_specs["storage"] = spec_value
            elif "gpu" in spec_name.lower():
                parsed_specs["gpu"] = spec_value
            elif "battery" in spec_name.lower():
                parsed_specs["battery"] = spec_value
            elif "weight" in spec_name.lower():
                parsed_specs["weight"] = spec_value
        
        laptop_list.append({
            "id": uri,
            "name": friendly_name,
            "specifications": parsed_specs
        })
    
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
    
@router.post("/track-interaction", status_code=status.HTTP_201_CREATED)
def track_interaction(events: List[BaseEventModel], db: Session = Depends(get_db)):
    """
    Track user interaction for recommendation system.
    laptop_id may or may not be present in event.data.
    """

    recommendation_service = RecommendationService(db)
    for event in events:
        recommendation_service.record_interaction(
            timestamp=event.timestamp,
            url=event.pageUrl,
            user_id=event.userId,
            session_id=event.sessionId,
            fingerprint=event.fingerprint,
            event_type = event.eventType,
            ip_address=event.ipAddress,
            user_agent=event.userAgent,
            device_info=event.deviceInfo,
            data = event.eventData
        )

    # Optionally, you can log or handle the missing laptop_id case here
    # For example:
    # if laptop_id is None:
    #     logger.warning("track_interaction called without laptop_id in event data")

    return {"message": "interaction recorded"}


@router.post("/is-first-time", status_code=status.HTTP_201_CREATED)
def track_interaction_first_time(fingerprint: FingerprintCheckRequest, db: Session = Depends(get_db)):
    
    # get cors on front end
    print(fingerprint)

    return {"message": "success", "data": {
        "firstTime": True
    } }
    
    #not get cors
    # print(fingerprint)

    # return {"status": "interaction recorded" }



@router.post("/track-interaction-first-time", status_code=status.HTTP_201_CREATED)
def track_interaction_first_time(events: List[BaseEventModel], db: Session = Depends(get_db)):    
    return {"status": "interaction recorded"}