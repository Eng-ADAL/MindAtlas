# ../mindatlas/src/extract.py
"""
MindAtlas Extract Layer

Responsible for communicating with the Joplin REST API and retrieving note data.
Implements pagination handling and defensive network behaviour to ensure
reliable data extraction in real-world conditions.

Responsibilities:
- Connect to Joplin API
- Retrieve notes with required fields
- Handle pagination until data is fully collected
- Provide resilience against timeouts, connection failures and HTTP errors
- Return a clean Python structure ready for transformation
"""


import requests
from config import BASE, TOKEN

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

        #when app mature remove this and use logging only
        print(f"Pulled page {page} -> {len(items)} notes")

        if payload.get("has_more") is False:
            break
        page +=1
    return all_items



