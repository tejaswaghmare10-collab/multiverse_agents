from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "agent_platform")

client: AsyncIOMotorClient = None


async def connect_db():
    """Connect to MongoDB on app startup."""
    global client
    client = AsyncIOMotorClient(MONGO_URI)
    print(f"✅ Connected to MongoDB: {MONGO_URI}")


async def close_db():
    """Close MongoDB connection on app shutdown."""
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed")


def get_db():
    """Return the database instance."""
    return client[DB_NAME]


def get_users_collection():
    """Return the users collection."""
    return get_db()["users"]