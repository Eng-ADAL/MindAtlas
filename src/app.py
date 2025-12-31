# mindatlass/src/app.py
"""
MindAtlas Application Orchestrator

Acts as the entry point for the data pipeline. Coordinates execution of
the Extract, Transform, Load workflow in a controlled and predictable way.

Responsibilities:
- Initialise pipeline execution
- Trigger note extraction from Joplin API
- Pass extracted data to transformation layer
- Handle errors cleanly to avoid silent failures
- Prepare for logging and orchestration enhancements in future phases
"""

import sys
from pprint import pprint

import extract      as ext
import transform    as tr
import load         as load
import config       as conf



def main():
    # ------------------------
    # Extract
    # ------------------------
    try:
        notes = ext.fetch_notes()
        print(f"\nPulled {len(notes)} notes from Joplin\n")
    except RuntimeError as e:
        print("Extraction failed")
        print(e)
        sys.exit(1)

    # Sample test
    print("Sample raw payload:")
    for note in notes[:3]:
        pprint({
            "id": note["id"],
            "title": note["title"],
            "created": note["created_time"]
        })

    # ------------------------
    #  Transform
    # ------------------------
    try:
        df = tr.transform_notes(notes)
    except RuntimeError as e:
        print("Transformation failed")
        print(e)
        sys.exit(1)

    print("\nTransformed dataframe preview:")
    print(df.head())
    print("\nSchema:")
    print(df.dtypes)
    print(f"\nTotal rows: {len(df)}")

    # ------------------------
    # Load (placeholder)
    # ------------------------
    # try:
    #     load.to_duckdb(df)
    # except RuntimeError as e:
    #     print("Load failed")
    #     print(e)
    #     sys.exit(1)


if __name__ == "__main__":
    main()
