# mindatlas/src/config.py
"""
MindAtlas Configuration Management

Central source of truth for application configuration.
Loads and validates environment variables required for runtime execution.

Responsibilities:
- Resolve project root paths
- Load .env configuration securely
- Expose Joplin API base URL and token
- Fail fast if required configuration is missing
- Provide a single location for future settings such as logging, feature flags,
  or multi-environment profiles
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Define directory and file paths
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

# Load environment
load_dotenv(ENV_PATH)

# Call .env file
BASE = os.getenv("JOPLIN_BASE")
TOKEN = os.getenv("JOPLIN_TOKEN")

# Call database
DB_PATH = os.getenv("DB_PATH", "mindatlas.duckdb")
NOTES_TABLE = "notes"

# Environmental parameters check
if not BASE or not TOKEN:
    raise RuntimeError("Joplin link or Joplin Token missing check .env file or read the documentation")




