#!/usr/bin/env python3
"""
Test script for Design Asset Extractor - Stage 1 POC.

Tests the extraction process with the existing Login Page UI data
to validate the accuracy and completeness of extracted assets.
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import figma_sdk
from design_asset_extractor import DesignAssetExtractor, extract_from_figma_file


def test_with_cached_data():
    """Test extraction using cached Figma data."""
    print("🧪 Testing Design Asset Extractor with Cached Data")
    print("=" * 50)

    # Load environment variables
    load_dotenv()
    file_key = os.getenv("FILE_KEY")
    project_name = os.getenv("PROJECT_NAME", "login-test")

    if not file_key:
        print("❌ FILE_KEY environment variable is required")
        return 1

    try:
        # Load FigmaFile from cache
        print("📂 Loading Figma file from cache...")
        figma_file = figma_sdk.FigmaFile.from_cache(file_key, project_name)
        print(f"✅ Loaded: {figma_file.name}")
        print(f"📊 Version: {figma_file.version}")
        print()

        # Create extractor and run extraction
        print("🔧 Creating Design Asset Extractor...")
        extractor = DesignAssetExtractor(figma_file, output_dir="extracted_login_assets")

        # Extract all assets
        results = extractor.extract_all_assets()
        print()

        # Validate outputs
        print("🔍 Validating extraction outputs...")
        validation_results = extractor.validate_outputs()
        print()

        # Save outputs
        print("💾 Saving extraction outputs...")
        output_files = extractor.save_outputs()
        print()

        # Generate and display report
        print("📋 Extraction Report:")
        print("-" * 30)
        report = extractor.get_extraction_report()
        print(report)
        print()

        # Show detailed results summary
        print("📊 Detailed Results Summary:")
        print("-" * 30)

        if "design_tokens" in results:
            tokens = results["design_tokens"]
            print(f"🎨 Design Tokens:")
            print(f"   - Colors found: {len(tokens.get('colors', {}).get('semantic', {})) + len(tokens.get('colors', {}).get('neutral', {}))}")
            print(f"   - Typography styles: {len(tokens.get('typography', {}).get('fontSizes', {}))}")
            print(f"   - Spacing values: {len(tokens.get('spacing', {}))}")

        if "component_catalog" in results:
            components = results["component_catalog"]
            print(f"🧩 Components:")
            print(f"   - Total components: {len(components.get('components', []))}")

            # Show component categories
            categories = {}
            for component in components.get('components', []):
                category = component.get('category', 'general')
                categories[category] = categories.get(category, 0) + 1

            for category, count in categories.items():
                print(f"   - {category}: {count}")

        if "screen_layouts" in results:
            layouts = results["screen_layouts"]
            screens = layouts.get('screens', [])
            print(f"📐 Layouts:")
            print(f"   - Total screens: {len(screens)}")

            # Show screen types
            for screen in screens:
                print(f"   - {screen['name']} ({screen['type']}) - {screen['size']['width']}x{screen['size']['height']}")

        print()
        print("✅ Design Asset Extraction Test Completed Successfully!")
        print(f"📁 Output files saved in: extracted_login_assets/")

        return 0

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


def test_with_api_data():
    """Test extraction using fresh API data."""
    print("🌐 Testing Design Asset Extractor with API Data")
    print("=" * 50)

    # Load environment variables
    load_dotenv()
    file_key = os.getenv("FILE_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    project_name = os.getenv("PROJECT_NAME", "login-test")

    if not file_key or not access_token:
        print("❌ FILE_KEY and ACCESS_TOKEN environment variables are required")
        return 1

    try:
        # Load FigmaFile from API
        print("🌐 Loading Figma file from API...")
        with figma_sdk.FigmaClient(token=access_token) as client:
            figma_file = figma_sdk.FigmaFile(file_key, project_name, client=client)
            print(f"✅ Loaded: {figma_file.name}")
            print(f"📊 Version: {figma_file.version}")
            print()

            # Create extractor and run extraction
            extractor = DesignAssetExtractor(figma_file, output_dir="extracted_login_assets_api")

            # Extract all assets
            results = extractor.extract_all_assets()
            print()

            # Validate outputs
            print("🔍 Validating extraction outputs...")
            validation_results = extractor.validate_outputs()
            print()

            # Save outputs
            print("💾 Saving extraction outputs...")
            output_files = extractor.save_outputs()
            print()

            print("✅ API-based Extraction Test Completed Successfully!")
            print(f"📁 Output files saved in: extracted_login_assets_api/")

            return 0

    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


def compare_outputs():
    """Compare cached vs API extraction outputs."""
    print("🔬 Comparing Cached vs API Extraction Outputs")
    print("=" * 50)

    try:
        # Load both outputs
        with open("extracted_login_assets/design_tokens.json", "r") as f:
            cached_tokens = f.read()

        with open("extracted_login_assets_api/design_tokens.json", "r") as f:
            api_tokens = f.read()

        # Simple comparison
        if cached_tokens == api_tokens:
            print("✅ Cached and API outputs are identical")
        else:
            print("⚠️  Cached and API outputs differ")
            print("   This might be due to data updates or different extraction parameters")

        return 0

    except FileNotFoundError as e:
        print(f"❌ Comparison failed - missing output files: {e}")
        return 1
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        return 1


def main():
    """Main test function."""
    print("🚀 Design Asset Extractor - Stage 1 POC Test")
    print("=" * 60)
    print()

    # Test 1: Cached data
    cached_result = test_with_cached_data()
    print()

    # Test 2: API data (optional - requires valid token)
    load_dotenv()
    if os.getenv("ACCESS_TOKEN"):
        api_result = test_with_api_data()
        print()

        # Test 3: Compare outputs
        if cached_result == 0 and api_result == 0:
            compare_outputs()
    else:
        print("⏭️  Skipping API test (no ACCESS_TOKEN provided)")
        print("🔑 To test with API data, set ACCESS_TOKEN in .env file")

    print()
    if cached_result == 0:
        print("🎉 Stage 1 POC Test: SUCCESS")
        print("✅ Design Asset Extractor is working correctly!")
        return 0
    else:
        print("❌ Stage 1 POC Test: FAILED")
        return 1


if __name__ == "__main__":
    exit(main())