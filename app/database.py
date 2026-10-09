import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in .env")

client = MongoClient(MONGO_URI)

db = client["ai_saas"]

users_collection = db["users"]
plans_collection = db["plans"]
subscriptions_collection = db["subscriptions"]
ai_tools_collection = db["ai_tools"]
ai_requests_collection = db["ai_requests"]
api_keys_collection = db["api_keys"]