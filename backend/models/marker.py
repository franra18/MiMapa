from typing import Optional
from pydantic import BaseModel

class MarkerBase(BaseModel):
    place_name: str  # Nombre del país o ciudad
    latitude: float
    longitude: float
    image_url: Optional[str] = None  # URL de la imagen en Cloudinary

class MarkerCreate(MarkerBase):
    pass

class MarkerResponse(MarkerBase):
    id: str
    user_email: str
