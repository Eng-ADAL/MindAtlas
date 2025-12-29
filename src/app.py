import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import sys

# Load environment
load_dotenv()

# Define directory and file paths
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH)

# Call .env file
BASE = os.getenv("JOPLIN_BASE")
TOKEN = os.getenv("JOPLIN_TOKEN")

# Environmental parameters check
if not BASE or not TOKEN:
    raise RuntimeError("Joplin link or Joplin Token missing check .env file or read the documentation")


# Pulling notes from joplin (limiting note pulling - for per API connection)
def fetch_notes(limit=30):
    url = f"{BASE}/notes"
    page = 1
    all_items = []

    while True:
        try:
            res = requests.get(
                url,
                params={
                    "token": TOKEN,
                    "fields": "id,title,created_time,updated_time,source_url,body",
                    "limit": limit,
                    "page": page
                },
                timeout=10
            )
            res.raise_for_status()
            payload = res.json()

        except requests.exceptions.Timeout:
            raise RuntimeError("Joplin API timed out. App not running or slow.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Cannot connect to Joplin. Service offline?")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP Error from Joplin: {e}")

        items = payload.get("items",[])
        all_items.extend(items)

        print(f"Pulled page {page} -> {len(items)} notes")

        if payload.get("has_more") is False:
            break
        page +=1
    return all_items

#a = fetch_notes()
#print(a)

try:
    notes = fetch_notes()
    print(f"Total pulled: {len(notes)}")
except RuntimeError as e:
    print(e)
    sys.exit(1)
