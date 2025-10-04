#!/usr/bin/env python3
"""
Simple Figma API cache - Just get and save JSON
"""

import json
from pathlib import Path
import requests

# Configuration
FILE_KEY = "BNYofc4IssIvloPwNRyJh4"
ACCESS_TOKEN = "YOUR_FIGMA_ACCESS_TOKEN"

if not FILE_KEY or not ACCESS_TOKEN:
    print("❌ Both file key and access token are required")
    exit(1)

print(f"🔍 Fetching file {FILE_KEY}...")

# API call
response = requests.get(
    f"https://api.figma.com/v1/files/{FILE_KEY}",
    headers={"X-Figma-Token": ACCESS_TOKEN}
)

if response.status_code != 200:
    print(f"❌ API Error: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()

# Save to file
output_file = Path(f"figma_{FILE_KEY}.json")
output_file.write_text(json.dumps(data, indent=2))

print(f"✅ Saved to {output_file}")
print(f"📊 File: {data.get('name')}")
print(f"🎨 Components: {len(data.get('components', {}))}")
print(f"📝 Styles: {len(data.get('styles', {}))}")