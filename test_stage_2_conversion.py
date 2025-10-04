#!/usr/bin/env python3
"""
Test script for Stage 2: Design System Converter.

Tests the complete conversion process using the Login Page UI data from Stage 1.
"""

import json
import sys
import os

# Add the design_system_converter to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from design_system_converter.converter import DesignSystemConverter


def main():
    """Run Stage 2 conversion test."""
    print("🧪 Testing Stage 2: Design System Converter")
    print("=" * 60)

    # Input and output paths
    input_path = "extracted_login_assets_api/all_assets.json"
    output_path = "stage_2_outputs"

    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        print("Please ensure Stage 1 extraction has been completed.")
        return False

    try:
        # Initialize converter
        converter = DesignSystemConverter()

        # Run conversion
        result = converter.run_conversion(input_path, output_path)

        if result['success']:
            print("\n🎉 Stage 2 conversion test completed successfully!")
            return True
        else:
            print("\n❌ Stage 2 conversion test failed!")
            return False

    except Exception as e:
        print(f"\n❌ Error during Stage 2 conversion test: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)