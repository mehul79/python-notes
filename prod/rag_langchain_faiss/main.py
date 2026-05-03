from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

print(api_key)