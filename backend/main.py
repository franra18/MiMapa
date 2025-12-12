from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, users, markers, visits
from starlette.middleware.sessions import SessionMiddleware
from .core.config import settings

app = FastAPI(title="Mi API de Producción")

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5174",
    settings.FRONTEND_URL,
    # Añade aquí tu dominio de producción (ej: https://mi-app.com)
]

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir Routers bajo el prefijo /api
app.include_router(auth.router, prefix="/api/auth")
app.include_router(users.router, prefix="/api")
app.include_router(markers.router, prefix="/api")
app.include_router(visits.router, prefix="/api")

@app.get("/api")
async def root():
    return {"message": "API funcionando correctamente"}