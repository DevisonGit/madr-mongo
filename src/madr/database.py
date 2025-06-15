from motor.motor_asyncio import AsyncIOMotorClient

from src.madr.settings import Settings

settings = Settings()
client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client['ap_mongo_db']
