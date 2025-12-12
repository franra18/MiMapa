from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.visit import VisitCreate, VisitResponse
from ..models.marker import MarkerResponse
from ..core.database import visits_collection, markers_collection, users_collection
from ..core.security import get_current_user
from ..models.user import UserBase
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/visits", tags=["Visits"])

@router.get("/user/{email}", response_model=List[MarkerResponse])
async def get_user_markers(
    email: str,
    current_user: UserBase = Depends(get_current_user)
):
    """Obtener los marcadores de otro usuario (para visualizar su mapa)"""
    # Verificar que el usuario visitado existe
    visited_user = await users_collection.find_one({"email": email})
    if not visited_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Registrar la visita (solo si no es el propio usuario)
    if email != current_user.email:
        visit_data = {
            "visitor_email": current_user.email,
            "visitor_oauth_token": current_user.username,  # Usamos username como token
            "visited_user_email": email,
            "timestamp": datetime.utcnow()
        }
        await visits_collection.insert_one(visit_data)
    
    # Obtener marcadores del usuario visitado
    markers = []
    async for marker in markers_collection.find({"user_email": email}):
        markers.append(MarkerResponse(
            id=str(marker["_id"]),
            user_email=marker["user_email"],
            place_name=marker["place_name"],
            latitude=marker["latitude"],
            longitude=marker["longitude"],
            image_url=marker.get("image_url")
        ))
    
    return markers

@router.get("/received", response_model=List[VisitResponse])
async def get_received_visits(current_user: UserBase = Depends(get_current_user)):
    """Obtener las visitas recibidas por el usuario actual, ordenadas por fecha"""
    visits = []
    async for visit in visits_collection.find(
        {"visited_user_email": current_user.email}
    ).sort("timestamp", -1):  # -1 = orden descendente (más recientes primero)
        visits.append(VisitResponse(
            id=str(visit["_id"]),
            visitor_email=visit["visitor_email"],
            visitor_oauth_token=visit["visitor_oauth_token"],
            visited_user_email=visit["visited_user_email"],
            timestamp=visit["timestamp"]
        ))
    
    return visits
