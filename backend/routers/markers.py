from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.marker import MarkerCreate, MarkerResponse
from core.database import markers_collection
from core.security import get_current_user
from models.user import UserBase
from bson import ObjectId

router = APIRouter(prefix="/markers", tags=["Markers"])

@router.get("/", response_model=List[MarkerResponse])
async def get_markers(current_user: UserBase = Depends(get_current_user)):
    """Obtener todos los marcadores del usuario actual"""
    markers = []
    async for marker in markers_collection.find({"user_email": current_user.email}):
        markers.append(MarkerResponse(
            id=str(marker["_id"]),
            user_email=marker["user_email"],
            place_name=marker["place_name"],
            latitude=marker["latitude"],
            longitude=marker["longitude"],
            image_url=marker.get("image_url")
        ))
    return markers

@router.post("/", response_model=MarkerResponse, status_code=201)
async def create_marker(
    marker: MarkerCreate,
    current_user: UserBase = Depends(get_current_user)
):
    """Crear un nuevo marcador para el usuario actual"""
    marker_data = {
        "user_email": current_user.email,
        "place_name": marker.place_name,
        "latitude": marker.latitude,
        "longitude": marker.longitude,
        "image_url": marker.image_url
    }
    
    result = await markers_collection.insert_one(marker_data)
    
    return MarkerResponse(
        id=str(result.inserted_id),
        **marker_data
    )

@router.delete("/{marker_id}", status_code=204)
async def delete_marker(
    marker_id: str,
    current_user: UserBase = Depends(get_current_user)
):
    """Eliminar un marcador del usuario actual"""
    try:
        object_id = ObjectId(marker_id)
    except:
        raise HTTPException(status_code=400, detail="ID de marcador inválido")
    
    result = await markers_collection.delete_one({
        "_id": object_id,
        "user_email": current_user.email
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Marcador no encontrado")
