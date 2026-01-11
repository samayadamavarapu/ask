from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from datetime import datetime
from typing import List, Dict, Any

settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        print(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")

    def close(self):
        if self.client:
            self.client.close()

    async def log_interaction(self, 
                              query: str, 
                              response: str, 
                              retrieved_chunks: List[str], 
                              safety_flag: str,
                              is_unsafe: bool = False):
        """
        Logs the user interaction.
        """
        if self.db is None:
            # Fallback or reconnect if needed, or raise error
            # For now, just print if not connected (dev mode safe)
            print("Warning: Database not connected. Log skipped.")
            return

        log_entry = {
            "query": query,
            "response": response,
            "retrieved_chunks": retrieved_chunks,
            "safety_flag": safety_flag,
            "is_unsafe": is_unsafe,
            "timestamp": datetime.utcnow()
        }
        
        await self.db.interactions.insert_one(log_entry)

db = MongoDB()
