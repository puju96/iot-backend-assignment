from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://<your-mongo-url>"  # use MongoDB Atlas free tier

client = AsyncIOMotorClient(MONGO_URL)
db = client.iot_db

users_collection = db.users
iot_collection = db.iot_data