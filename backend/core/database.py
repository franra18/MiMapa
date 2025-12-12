from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DB_NAME]
users_collection = db.users
markers_collection = db.markers
visits_collection = db.visits