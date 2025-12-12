from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from core.config import settings
from core.database import users_collection
from core.security import create_access_token
from models.user import UserBase
from datetime import timedelta
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["Auth"])

# Configuración de OAuth con Google
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# 1. Endpoint que inicia el login (Redirige a Google)
@router.get("/login/google")
async def login_google(request: Request):
    # Redirige al usuario a la URL de Google.
    # El redirect_uri debe coincidir EXACTAMENTE con el puesto en Google Console
    redirect_uri = request.url_for('auth_google') 
    return await oauth.google.authorize_redirect(request, redirect_uri)

# 2. Endpoint de Callback (Google nos devuelve aquí)
@router.get("/google/callback")
async def auth_google(request: Request):
    try:
        # Obtener token de Google
        token = await oauth.google.authorize_access_token(request)
        
        # Obtener datos del usuario desde Google
        user_info = token.get('userinfo')
        if not user_info:
             user_info = await oauth.google.userinfo(token=token) # Fallback

        email = user_info.get("email")
        
        # LÓGICA DE BASE DE DATOS (Upsert)
        # Buscamos si el usuario ya existe por email
        user_doc = await users_collection.find_one({"email": email})
        
        if not user_doc:
            # Si no existe, lo creamos automáticamente
            new_user = {
                "username": email.split("@")[0], # Usamos parte del email como username
                "email": email,
                "provider": "google", # Marcamos que viene de google
                "disabled": False,
                # No guardamos password porque usa Google
            }
            await users_collection.insert_one(new_user)
            user_doc = new_user

        # GENERAMOS NUESTRO PROPIO TOKEN (El que tu frontend ya sabe usar)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_doc["username"]}, # O usa el email como 'sub'
            expires_delta=access_token_expires
        )

        # REDIRECCIÓN AL FRONTEND
        # Enviamos el token en la URL para que Vue lo capture
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth-callback?token={access_token}")

    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=400, detail=f"Error en login con Google: {str(e)}")