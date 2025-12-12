# Estructura del Proyecto MiMapa

## 📁 Árbol de Directorios

```
MiMapa/
├── backend/                          # API FastAPI (Python)
│   ├── core/                         # Configuración y servicios centrales
│   │   ├── config.py                 # Variables de entorno y settings
│   │   ├── database.py               # Conexión MongoDB (Motor)
│   │   └── security.py               # JWT, hashing, autenticación
│   │
│   ├── models/                       # Modelos Pydantic
│   │   ├── user.py                   # Usuario (email, username, provider)
│   │   ├── marker.py                 # Marcador en mapa (lat, lon, imagen)
│   │   ├── visit.py                  # Visita entre usuarios
│   │   └── token.py                  # Token JWT
│   │
│   ├── routers/                      # Endpoints de la API
│   │   ├── auth.py                   # Login con Google OAuth
│   │   ├── users.py                  # Perfil de usuario (/users/me)
│   │   ├── markers.py                # CRUD de marcadores
│   │   └── visits.py                 # Gestión de visitas
│   │
│   ├── dependencies.py               # Dependencias (get_current_user)
│   ├── main.py                       # Entry point de FastAPI
│   └── requirements.txt              # Dependencias Python
│
├── frontend/
│   └── vue-frontend/                 # Cliente Vue.js + Ionic
│       ├── public/                   # Archivos estáticos
│       │
│       ├── src/
│       │   ├── assets/               # Imágenes, iconos
│       │   │
│       │   ├── components/           # Componentes reutilizables
│       │   │   ├── AddPlaceForm.vue  # Formulario para añadir marcador
│       │   │   ├── ImageUpload.vue   # Subida de imágenes a Cloudinary
│       │   │   ├── MapView.vue       # Mapa interactivo (Leaflet)
│       │   │   ├── VisitsList.vue    # Lista de visitas recibidas
│       │   │   └── VisitUserForm.vue # Formulario visitar usuario
│       │   │
│       │   ├── views/                # Páginas principales
│       │   │   ├── Login.vue         # Login con Google
│       │   │   ├── AuthCallback.vue  # Callback OAuth (guarda token)
│       │   │   ├── Dashboard.vue     # Panel principal (mapa + marcadores)
│       │   │   └── VisitMap.vue      # Ver mapa de otro usuario
│       │   │
│       │   ├── router/               # Configuración de rutas
│       │   │   └── index.js          # Vue Router + guards de auth
│       │   │
│       │   ├── services/             # Lógica de API
│       │   │   ├── api.js            # Cliente Axios configurado
│       │   │   ├── marker.js         # Servicios de marcadores
│       │   │   └── visit.js          # Servicios de visitas
│       │   │
│       │   ├── App.vue               # Componente raíz
│       │   ├── main.js               # Entry point de Vue
│       │   └── style.css             # Estilos globales
│       │
│       ├── .env                      # Variables de entorno (frontend)
│       ├── package.json              # Dependencias npm
│       ├── vite.config.js            # Configuración Vite
│       └── index.html                # HTML base
│
├── AGENTS.md                         # Guía de desarrollo completa
└── ESTRUCTURA.md                     # Este archivo
```

---

## 🏗️ Arquitectura del Sistema

### Backend (Monolito Modular)

```
┌─────────────────────────────────────────────────────┐
│                    FastAPI App                       │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Routers   │  │     Core     │  │   Models   │ │
│  │             │  │              │  │            │ │
│  │ • auth      │  │ • config     │  │ • user     │ │
│  │ • users     │  │ • database   │  │ • marker   │ │
│  │ • markers   │  │ • security   │  │ • visit    │ │
│  │ • visits    │  │              │  │ • token    │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │        Middleware (CORS + Sessions)          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         ↓                    ↓
   ┌──────────┐        ┌─────────────┐
   │ MongoDB  │        │   Google    │
   │  Atlas   │        │   OAuth     │
   └──────────┘        └─────────────┘
```

### Frontend (SPA)

```
┌─────────────────────────────────────────────────────┐
│                  Vue.js 3 App                        │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │    Views    │  │  Components  │  │  Services  │ │
│  │             │  │              │  │            │ │
│  │ • Login     │  │ • MapView    │  │ • api      │ │
│  │ • Dashboard │  │ • ImageUp.   │  │ • marker   │ │
│  │ • VisitMap  │  │ • AddPlace   │  │ • visit    │ │
│  │ • AuthCall. │  │ • VisitsList │  │            │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │         Vue Router (Navigation Guards)       │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         ↓                    ↓                ↓
   ┌──────────┐      ┌────────────┐   ┌──────────┐
   │ Backend  │      │ Cloudinary │   │   OSM    │
   │   API    │      │  (Images)  │   │  (Maps)  │
   └──────────┘      └────────────┘   └──────────┘
```

---

## 🔄 Flujo de Datos Principal

### 1️⃣ Autenticación (Google OAuth)

```
Usuario → Click "Login Google"
   ↓
Frontend → Redirige a: /auth/login/google
   ↓
Backend → Redirige a: Google OAuth
   ↓
Google → Usuario autoriza → Callback: /auth/google/callback
   ↓
Backend → Valida token de Google
        → Upsert usuario en MongoDB
        → Genera JWT propio
        → Redirige a: /auth-callback?token=JWT
   ↓
Frontend → Guarda JWT en localStorage
         → Redirige a: /dashboard
```

### 2️⃣ Crear Marcador con Imagen

```
Usuario → Selecciona ubicación en mapa (Leaflet)
        → Sube imagen
   ↓
Frontend → Valida archivo < 5MB
         → Sube a Cloudinary (unsigned)
         → Obtiene secure_url
   ↓
Frontend → POST /markers
         → { lat, lon, place_name, image_url }
         → Header: Authorization: Bearer JWT
   ↓
Backend → Valida JWT (get_current_user)
        → Extrae user_email del token
        → Guarda en MongoDB
   ↓
MongoDB → { user_email, lat, lon, place_name, image_url, _id }
   ↓
Frontend → Recibe marcador creado
         → Actualiza mapa en tiempo real
```

### 3️⃣ Visitar Mapa de Otro Usuario

```
Usuario → Ingresa email en formulario
   ↓
Frontend → GET /visits/user/{email}
         → Header: Authorization: Bearer JWT
   ↓
Backend → Valida JWT
        → Verifica que el usuario visitado existe
        → Registra visita en MongoDB (si no es el mismo usuario)
        → Devuelve marcadores del usuario visitado
   ↓
Frontend → Muestra mapa con marcadores
         → Modo "solo lectura"
```

---

## 🗄️ Esquema de Base de Datos (MongoDB)

### Colección: `users`

```json
{
  "_id": ObjectId,
  "username": "franramirez",
  "email": "franramirez@gmail.com",
  "provider": "google",
  "disabled": false,
  "created_at": ISODate
}
```

### Colección: `markers`

```json
{
  "_id": ObjectId,
  "user_email": "franramirez@gmail.com",
  "place_name": "Mi Casa",
  "latitude": 40.4165,
  "longitude": -3.7026,
  "image_url": "https://res.cloudinary.com/...",
  "created_at": ISODate
}
```

### Colección: `visits`

```json
{
  "_id": ObjectId,
  "visitor_email": "juan@gmail.com",
  "visitor_oauth_token": "juan",
  "visited_user_email": "franramirez@gmail.com",
  "timestamp": ISODate
}
```

---

## 🔐 Variables de Entorno

### Backend (`.env`)

```env
# MongoDB Atlas
MONGO_URL=mongodb+srv://user:password@cluster.mongodb.net/
DB_NAME=Parcial2

# JWT
SECRET_KEY=tu_secret_key_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth
GOOGLE_CLIENT_ID=143980033944-...apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-...

# Frontend
FRONTEND_URL=http://localhost:5173
```

### Frontend (`.env`)

```env
# API Backend
VITE_API_URL=http://localhost:8000

# Google OAuth (mismo Client ID que backend)
VITE_GOOGLE_CLIENT_ID=143980033944-...apps.googleusercontent.com

# Cloudinary (Subida de imágenes)
VITE_CLOUDINARY_CLOUD_NAME=dxeq2angp
VITE_CLOUDINARY_UPLOAD_PRESET=examen
```

---

## 🚀 Endpoints de la API

### Autenticación (`/auth`)

| Método | Ruta                    | Descripción                        |
|--------|-------------------------|------------------------------------|
| GET    | `/auth/login/google`    | Inicia login con Google OAuth      |
| GET    | `/auth/google/callback` | Callback de Google (genera JWT)    |

### Usuarios (`/users`)

| Método | Ruta        | Descripción                     |
|--------|-------------|---------------------------------|
| GET    | `/users/me` | Obtiene perfil del usuario actual (requiere auth) |

### Marcadores (`/markers`)

| Método | Ruta             | Descripción                |
|--------|------------------|----------------------------|
| GET    | `/markers`       | Lista marcadores del usuario |
| POST   | `/markers`       | Crea nuevo marcador        |
| DELETE | `/markers/{id}`  | Elimina marcador           |

### Visitas (`/visits`)

| Método | Ruta                    | Descripción                        |
|--------|-------------------------|------------------------------------|
| GET    | `/visits/user/{email}`  | Obtiene marcadores de otro usuario |
| GET    | `/visits/received`      | Obtiene visitas recibidas          |

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno para Python
- **Motor**: Driver async de MongoDB
- **Authlib**: Manejo de OAuth 2.0
- **PyJWT**: Generación y validación de tokens JWT
- **Pydantic**: Validación de datos

### Frontend
- **Vue.js 3**: Framework JavaScript progresivo
- **Ionic Framework 8**: UI components móviles
- **Vue Router**: Navegación SPA
- **Axios**: Cliente HTTP
- **Leaflet**: Mapas interactivos
- **Vite**: Build tool

### Servicios Externos
- **MongoDB Atlas**: Base de datos cloud
- **Google Cloud (OAuth)**: Autenticación
- **Cloudinary**: Almacenamiento de imágenes
- **OpenStreetMap**: Tiles de mapas
- **Nominatim**: Geocodificación

---

## 📦 Comandos de Desarrollo

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend/vue-frontend
npm install
npm run dev  # Corre en puerto 5173
```

---

## 🔒 Seguridad Implementada

1. **JWT Authentication**: Tokens firmados con HS256
2. **OAuth 2.0**: Delegación de autenticación en Google
3. **CORS Middleware**: Control de orígenes permitidos
4. **Session Middleware**: Gestión segura de sesiones
5. **Password Hashing**: bcrypt (aunque Google OAuth no usa passwords)
6. **Environment Variables**: Credenciales nunca en código
7. **Navigation Guards**: Protección de rutas en frontend

---

## 📝 Notas Importantes

- **Arquitectura Monolítica**: Backend en un solo proceso FastAPI
- **SPA (Single Page Application)**: Frontend en Vue Router
- **Serverless Ready**: Compatible con despliegues serverless
- **Mobile First**: Diseñado con Ionic para web y móvil
- **RESTful API**: Endpoints siguiendo convenciones REST
