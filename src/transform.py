# mindatlas/src/transform.py
"""
MindAtlas Transform Layer

Converts raw extracted Joplin notes into a structured and analysable format
using Pandas. Normalises fields and ensures predictable schema output so
downstream systems can rely on stable data contracts.

Responsibilities:
- Convert Python list of note objects into DataFrame
- Normalise timestamps and ensure consistent datatypes
- Standardise column naming and ordering
- Prepare data for database loading and analytics
- Remain deliberately boring and reliable
"""

import pandas   as pd
import datetime as datetime

def transform_notes(notes):
    """
    Transform raw Joplin notes into a clean Pandas DataFrame.

    - Validates payload
    - Normalises timestamps
    - Renames fields to stable names
    - Adds useful derived fields

    Returns:
        pd.DataFrame
    """
    if not notes:
        raise RuntimeError("Transform received empty payload. Extraction likely failed.")

    # Build dataframe
    df = pd.DataFrame(notes)

    # Normalise timestamps
    df["created_time"] = pd.to_datetime(df["created_time"], unit="ms")
    df["updated_time"] = pd.to_datetime(df["updated_time"], unit="ms")

    # Rename to human-friendly names
    df.rename(
        columns={
            "created_time": "created_at",
            "updated_time": "updated_at"
        },
        inplace=True
    )

    # Null safety
    df["title"] = df["title"].fillna("")
    df["body"] = df["body"].fillna("")
    df["source_url"] = df["source_url"].fillna("")

    # Useful computed fields
    df["body_length"] = df["body"].str.len()
    df["has_source"] = df["source_url"] != ""
    df["created_date"] = df["created_at"].dt.date

    return df

