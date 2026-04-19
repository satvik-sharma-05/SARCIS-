"""Database connection"""
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "sarcis")

client = None
database = None


async def init_db():
    """Initialize database connection"""
    global client, database
    client = AsyncIOMotorClient(MONGO_URI)
    database = client[DB_NAME]
    
    # Create indexes
    await database.users.create_index("email", unique=True)
    await database.clusters.create_index("user_id")
    await database.files.create_index("cluster_id")
    await database.results.create_index("cluster_id")


async def get_db():
    """Get database instance"""
    return database
