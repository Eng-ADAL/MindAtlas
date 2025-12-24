import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment
load_dotenv()

# Define directory and file paths
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH)

# Cal .env file 
BASE = os.getenv("JOPLIN_BASE")
TOKEN = os.getenv("JOPLIN_TOKEN")

if not BASE or not TOKEN:
    raise RuntimeError("Joplin link or Joplin Token missing check .env file or read the documentation")

res = requests.get(
    f"{BASE}/notes",
    params={"token": TOKEN},
    timeout=10
)

print("Status", res.status_code)
print(res.json())


