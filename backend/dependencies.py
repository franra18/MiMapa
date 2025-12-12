from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.config import settings
from core.database import users_collection
from models.user import UserBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token") # Nota el cambio en la URL

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_doc = await users_collection.find_one({"username": username})
    if user_doc is None:
        raise credentials_exception
    
    return UserBase(**user_doc)