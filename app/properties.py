import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Properties:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
properties = Properties()