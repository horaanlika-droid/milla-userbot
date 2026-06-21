import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
PHONE = os.getenv('PHONE', '')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')