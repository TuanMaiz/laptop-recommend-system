from pydantic import BaseModel


class FingerprintCheckRequest(BaseModel):
    fingerprint: str;
    
    
class FirstTimeReference(BaseModel):
    fingerprint: str;
    Functionality: str;
    priceRange: str;
    brand: str;
