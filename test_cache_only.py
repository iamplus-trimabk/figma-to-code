#!/usr/bin/env python3
"""
Test loading from cache only - demonstrates offline capability.
"""

import os
from dotenv import load_dotenv
from figma_sdk import FigmaFile

def test_cache_only():
    """Test loading FigmaFile from cache without API access."""
    print("🗂️  Cache-Only Test")
    print("=" * 30)

    load_dotenv()
    file_key = os.getenv("FILE_KEY")
    project_name = os.getenv("PROJECT_NAME", "default")

    if not file_key:
        print("❌ FILE_KEY environment variable is required")
        return 1

    print(f"📁 Project: {project_name}")
    print(f"🔑 File Key: {file_key}")
    print()

    try:
        # Load from cache only
        print("📂 Loading from cache...")
        figma_file = FigmaFile.from_cache(file_key, project_name)

        print(f"✅ Loaded from cache: {figma_file.name}")
        print(f"📊 Version: {figma_file.version}")
        print(f"🕒 Last Modified: {figma_file.last_modified}")
        print(f"🧩 Components: {figma_file.components_count}")
        print(f"🎨 Styles: {figma_file.styles_count}")

        # Test data access
        print("\n🔍 Accessing cached data:")
        document = figma_file.document
        print(f"   Document type: {document.get('type')}")
        print(f"   Document ID: {document.get('id')}")

        # Show color styles
        color_styles = figma_file.get_color_styles()
        print(f"   Color styles found: {len(color_styles)}")
        for style in color_styles:
            print(f"     • {style['name']}")

        # Show text styles
        text_styles = figma_file.get_text_styles()
        print(f"   Text styles found: {len(text_styles)}")
        for style in text_styles:
            print(f"     • {style['name']}")

        # Test node finding (this will work with cached data)
        frames = figma_file.find_node_by_type("FRAME")
        print(f"   Frames found: {len(frames)}")
        for frame in frames[:3]:  # Show first 3
            print(f"     • {frame['name']} ({frame.get('type', 'Unknown')})")

        print(f"\n✨ Cache-only access successful!")
        return 0

    except FileNotFoundError as e:
        print(f"❌ Cache file not found: {e}")
        print("   Run consumer_example.py first to cache the file")
        return 1

    except Exception as e:
        print(f"❌ Error loading from cache: {e}")
        return 1


if __name__ == "__main__":
    exit(test_cache_only())