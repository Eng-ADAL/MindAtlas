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

# Call .env file
BASE = os.getenv("JOPLIN_BASE")
TOKEN = os.getenv("JOPLIN_TOKEN")

if not BASE or not TOKEN:
    raise RuntimeError("Joplin link or Joplin Token missing check .env file or read the documentation")

def fetch_notes():
    url = f"{BASE}/notes"
    # down below don't we need try except block? if res can't conenct to joplin it should say can't connect not running?
    res = requests.get(
        url,
        params={
            "token": TOKEN,
            "fields": "id,title,created_time,updated_time,source_url,body",
            "limit": 50
            },
        timeout=10
    )

    try:
        res.raise_for_status()
        return res.json()

    except requests.exceptions.Timeout:
        raise RuntimeError("Joplin API time out. App not running or slow")

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Cannot connect to Joplin. May service offline?")

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP Error from Joplin: {e}")


data = fetch_notes()
print("Status: OK")
print(len(data.get("items", [])), "notes pulled succesfully")
