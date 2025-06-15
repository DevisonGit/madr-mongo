from motor.motor_asyncio import AsyncIOMotorClient

from src.madr.settings import Settings

settings = Settings()
client = AsyncIOMotorClient(settings.DATABASE_URL)  # Exemplo: mongodb://mongo:27017
db = client["ap_mongo_db"]  # Substitua com o nome real do seu banco
