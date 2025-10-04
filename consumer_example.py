#!/usr/bin/env python3
"""
Consumer example using the Figma SDK with .env configuration.

Demonstrates clean, professional usage of the Figma SDK.
"""

import os
from dotenv import load_dotenv
from figma_sdk import FigmaClient, FigmaFile
from figma_sdk.exceptions import FigmaAPIError, FigmaAuthError


def main():
    """Main consumer function demonstrating SDK usage."""
    print("🚀 Figma SDK Consumer Example")
    print("=" * 40)

    # Load environment variables
    load_dotenv()

    # Get configuration from environment
    file_key = os.getenv("FILE_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    project_name = os.getenv("PROJECT_NAME", "default")

    if not file_key:
        print("❌ FILE_KEY environment variable is required")
        return 1

    if not access_token:
        print("❌ ACCESS_TOKEN environment variable is required")
        return 1

    print(f"📁 Project: {project_name}")
    print(f"🔑 File Key: {file_key}")
    print()

    try:
        # Initialize Figma client
        print("🔌 Initializing Figma client...")
        with FigmaClient(token=access_token) as client:
            print("✅ Client initialized successfully")

            # Create FigmaFile instance
            print("\n📄 Loading Figma file...")
            figma_file = FigmaFile(
                file_key=file_key,
                project_name=project_name,
                client=client
            )

            print(f"✅ File loaded: {figma_file.name}")
            print(f"📊 Version: {figma_file.version}")
            print(f"🕒 Last Modified: {figma_file.last_modified}")
            print(f"🧩 Components: {figma_file.components_count}")
            print(f"🎨 Styles: {figma_file.styles_count}")

            # Get file information
            print("\n📋 File Information:")
            print(f"   Name: {figma_file.name}")
            print(f"   File Key: {figma_file.file_key}")
            print(f"   Thumbnail: {figma_file.thumbnail_url}")

            # Get pages
            print("\n📑 Pages:")
            pages = figma_file.get_pages()
            for i, page in enumerate(pages, 1):
                print(f"   {i}. {page['name']} ({page['children_count']} children)")

            # Get color styles
            print("\n🎨 Color Styles:")
            color_styles = figma_file.get_color_styles()
            for style in color_styles[:5]:  # Show first 5
                print(f"   • {style['name']}")
            if len(color_styles) > 5:
                print(f"   ... and {len(color_styles) - 5} more")

            # Get text styles
            print("\n📝 Text Styles:")
            text_styles = figma_file.get_text_styles()
            for style in text_styles[:5]:  # Show first 5
                print(f"   • {style['name']}")
            if len(text_styles) > 5:
                print(f"   ... and {len(text_styles) - 5} more")

            # Search for components by type
            print("\n🔍 Component Analysis:")
            try:
                frames = figma_file.find_node_by_type("FRAME")
                print(f"   Frames found: {len(frames)}")

                components = figma_file.find_node_by_type("COMPONENT")
                print(f"   Components found: {len(components)}")

                instances = figma_file.find_node_by_type("INSTANCE")
                print(f"   Component instances found: {len(instances)}")

            except Exception as e:
                print(f"   ⚠️  Component analysis failed: {e}")

            # Export to cache
            print("\n💾 Exporting to cache...")
            cache_path = figma_file.export_to_cache()
            print(f"✅ Cached to: {cache_path}")

            # Show cache statistics
            print("\n📈 Cache Statistics:")
            stats = client.get_usage_stats()
            cache_stats = stats['cache_stats']
            print(f"   Total entries: {cache_stats['total_entries']}")
            print(f"   Valid entries: {cache_stats['valid_entries']}")
            print(f"   Cache size: {cache_stats['total_size_bytes']} bytes")
            print(f"   Health check: {'✅' if stats['health_check'] else '❌'}")

            print(f"\n✨ Operation completed successfully!")
            return 0

    except FigmaAuthError as e:
        print(f"❌ Authentication Error: {e}")
        print("   Please check your ACCESS_TOKEN in .env file")
        return 1

    except FigmaAPIError as e:
        print(f"❌ API Error: {e}")
        if e.status_code == 404:
            print(f"   File '{file_key}' not found or access denied")
        return 1

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return 1


def demo_cache_usage():
    """Demonstrate loading from cache without API access."""
    print("\n🗂️  Cache Usage Demo:")
    print("-" * 30)

    load_dotenv()
    file_key = os.getenv("FILE_KEY")
    project_name = os.getenv("PROJECT_NAME", "default")

    try:
        # Try to load from cache
        cached_file = FigmaFile.from_cache(file_key, project_name)
        print(f"✅ Loaded from cache: {cached_file.name}")
        print(f"   Components: {cached_file.components_count}")
        print(f"   Styles: {cached_file.styles_count}")
        return True

    except FileNotFoundError:
        print("ℹ️  No cached file found. Run main() first to cache the file.")
        return False
    except Exception as e:
        print(f"❌ Cache loading failed: {e}")
        return False


if __name__ == "__main__":
    # Run main example
    exit_code = main()

    # Demonstrate cache usage
    if exit_code == 0:
        demo_cache_usage()

    exit(exit_code)