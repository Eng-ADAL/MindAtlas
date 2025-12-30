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

import os
import sys

import extract      as ext
import transform    as tr
import load         as load
import config       as conf

#a = fetch_notes()
#print(a)

try:
    notes = ext.fetch_notes()
    print(f"Total pulled: {len(notes)}")
except RuntimeError as e:
    print(e)
    print("\n\nExtraction failed!")
    sys.exit(1)

"""
# Place holder for transform and load steps
try:
    df = tr.transform_notes(notes)
except RuntimeError as e:
    print("\n\nTransformation failed!")
    print(e)
    sys.exit

try:
    load.to_duckdb(df)
except RuntimeError as e:
    print("\n\nTransformation failed!")
    print(e)
    sys.exit
"""




