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

import pandas

