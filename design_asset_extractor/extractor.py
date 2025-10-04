"""
Design Asset Extractor - Main orchestrator for Stage 1.

Coordinates the extraction of design tokens, components, and layouts
from Figma designs and outputs structured JSON for downstream stages.
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add parent directory to path for figma_sdk import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import figma_sdk
from .token_extractor import TokenExtractor
from .component_parser import ComponentParser
from .layout_analyzer import LayoutAnalyzer
from .schemas import DesignAssetSchemas


class DesignAssetExtractor:
    """Main orchestrator for design asset extraction."""

    def __init__(self, figma_file: 'figma_sdk.files.FigmaFile', output_dir: str = "extracted_assets"):
        """Initialize with FigmaFile and output directory."""
        self.figma_file = figma_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize extractors
        self.token_extractor = TokenExtractor(figma_file)
        self.component_parser = ComponentParser(figma_file)
        self.layout_analyzer = LayoutAnalyzer(figma_file)

        # Storage for results
        self.extraction_results: Dict[str, Any] = {}
        self.extraction_metadata: Dict[str, Any] = {}

    def extract_all_assets(self) -> Dict[str, Any]:
        """Extract all design assets from the Figma file."""
        print("🚀 Starting design asset extraction...")
        print(f"📁 File: {self.figma_file.name}")
        print(f"🔑 File Key: {self.figma_file.file_key}")
        print()

        # Record extraction start time
        start_time = datetime.now()
        self.extraction_metadata["start_time"] = start_time.isoformat()
        self.extraction_metadata["figma_file"] = {
            "name": self.figma_file.name,
            "file_key": self.figma_file.file_key,
            "version": self.figma_file.version,
            "last_modified": self.figma_file.last_modified
        }

        try:
            # Extract design tokens
            print("🎨 Step 1: Extracting design tokens...")
            design_tokens = self.token_extractor.extract_all_tokens()
            self.extraction_results["design_tokens"] = design_tokens
            token_summary = self.token_extractor.get_token_summary()
            print(f"   ✅ Colors: {token_summary['colors']}")
            print(f"   ✅ Typography tokens: {token_summary['typography_tokens']}")
            print(f"   ✅ Spacing values: {token_summary['spacing_values']}")
            print()

            # Extract components
            print("🧩 Step 2: Parsing components...")
            component_catalog = self.component_parser.parse_all_components()
            self.extraction_results["component_catalog"] = component_catalog
            component_summary = self.component_parser.get_component_summary()
            print(f"   ✅ Total components: {component_summary['total_components']}")
            print(f"   ✅ Components with variants: {component_summary['with_variants']}")
            if component_summary['by_category']:
                print(f"   ✅ Categories: {', '.join(component_summary['by_category'].keys())}")
            print()

            # Extract layouts
            print("📐 Step 3: Analyzing layouts...")
            screen_layouts = self.layout_analyzer.analyze_all_layouts()
            self.extraction_results["screen_layouts"] = screen_layouts
            layout_summary = self.layout_analyzer.get_layout_summary()
            print(f"   ✅ Screens: {layout_summary['total_screens']}")
            print(f"   ✅ Unique screen sizes: {layout_summary['screen_sizes']['unique_sizes']}")
            print(f"   ✅ Layout types: {', '.join(layout_summary['layout_types'].keys()) if layout_summary['layout_types'] else 'None'}")
            print()

            # Record completion time
            end_time = datetime.now()
            self.extraction_metadata["end_time"] = end_time.isoformat()
            self.extraction_metadata["duration_seconds"] = (end_time - start_time).total_seconds()
            self.extraction_metadata["status"] = "success"

            # Generate summary
            self._generate_extraction_summary(token_summary, component_summary, layout_summary)

            print("✨ Design asset extraction completed successfully!")
            return self.extraction_results

        except Exception as e:
            # Record error
            self.extraction_metadata["end_time"] = datetime.now().isoformat()
            self.extraction_metadata["status"] = "error"
            self.extraction_metadata["error"] = str(e)
            print(f"❌ Extraction failed: {e}")
            raise

    def _generate_extraction_summary(self, token_summary: Dict, component_summary: Dict, layout_summary: Dict) -> None:
        """Generate extraction summary."""
        self.extraction_metadata["summary"] = {
            "design_tokens": token_summary,
            "components": component_summary,
            "layouts": layout_summary
        }

    def save_outputs(self, indent: int = 2) -> Dict[str, Path]:
        """Save all extraction outputs to JSON files."""
        if not self.extraction_results:
            raise ValueError("No extraction results to save. Run extract_all_assets() first.")

        output_files = {}

        # Save design tokens
        design_tokens_file = self.output_dir / "design_tokens.json"
        with open(design_tokens_file, 'w', encoding='utf-8') as f:
            json.dump(self.extraction_results["design_tokens"], f, indent=indent, ensure_ascii=False)
        output_files["design_tokens"] = design_tokens_file
        print(f"💾 Saved design tokens: {design_tokens_file}")

        # Save component catalog
        component_catalog_file = self.output_dir / "component_catalog.json"
        with open(component_catalog_file, 'w', encoding='utf-8') as f:
            json.dump(self.extraction_results["component_catalog"], f, indent=indent, ensure_ascii=False)
        output_files["component_catalog"] = component_catalog_file
        print(f"💾 Saved component catalog: {component_catalog_file}")

        # Save screen layouts
        screen_layouts_file = self.output_dir / "screen_layouts.json"
        with open(screen_layouts_file, 'w', encoding='utf-8') as f:
            json.dump(self.extraction_results["screen_layouts"], f, indent=indent, ensure_ascii=False)
        output_files["screen_layouts"] = screen_layouts_file
        print(f"💾 Saved screen layouts: {screen_layouts_file}")

        # Save extraction metadata
        metadata_file = self.output_dir / "extraction_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.extraction_metadata, f, indent=indent, ensure_ascii=False)
        output_files["metadata"] = metadata_file
        print(f"💾 Saved extraction metadata: {metadata_file}")

        # Save combined output
        combined_output_file = self.output_dir / "all_assets.json"
        combined_output = {
            "metadata": self.extraction_metadata,
            "design_tokens": self.extraction_results["design_tokens"],
            "component_catalog": self.extraction_results["component_catalog"],
            "screen_layouts": self.extraction_results["screen_layouts"]
        }
        with open(combined_output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_output, f, indent=indent, ensure_ascii=False)
        output_files["combined"] = combined_output_file
        print(f"💾 Saved combined output: {combined_output_file}")

        return output_files

    def validate_outputs(self) -> Dict[str, bool]:
        """Validate extraction outputs against schemas."""
        if not self.extraction_results:
            raise ValueError("No extraction results to validate. Run extract_all_assets() first.")

        validation_results = {}

        # Validate design tokens
        if "design_tokens" in self.extraction_results:
            design_tokens_valid = DesignAssetSchemas.validate_output(
                self.extraction_results["design_tokens"],
                "design_tokens"
            )
            validation_results["design_tokens"] = design_tokens_valid
            print(f"🔍 Design tokens validation: {'✅' if design_tokens_valid else '❌'}")

        # Validate component catalog
        if "component_catalog" in self.extraction_results:
            component_catalog_valid = DesignAssetSchemas.validate_output(
                self.extraction_results["component_catalog"],
                "component_catalog"
            )
            validation_results["component_catalog"] = component_catalog_valid
            print(f"🔍 Component catalog validation: {'✅' if component_catalog_valid else '❌'}")

        # Validate screen layouts
        if "screen_layouts" in self.extraction_results:
            screen_layouts_valid = DesignAssetSchemas.validate_output(
                self.extraction_results["screen_layouts"],
                "screen_layouts"
            )
            validation_results["screen_layouts"] = screen_layouts_valid
            print(f"🔍 Screen layouts validation: {'✅' if screen_layouts_valid else '❌'}")

        return validation_results

    def get_extraction_report(self) -> str:
        """Generate a human-readable extraction report."""
        if not self.extraction_metadata:
            return "No extraction data available."

        report = []
        report.append("# Design Asset Extraction Report")
        report.append(f"**Figma File**: {self.extraction_metadata['figma_file']['name']}")
        report.append(f"**File Key**: {self.extraction_metadata['figma_file']['file_key']}")
        report.append(f"**Status**: {self.extraction_metadata['status']}")
        report.append(f"**Duration**: {self.extraction_metadata.get('duration_seconds', 'N/A')} seconds")
        report.append("")

        if "summary" in self.extraction_metadata:
            summary = self.extraction_metadata["summary"]

            # Design tokens summary
            if "design_tokens" in summary:
                tokens = summary["design_tokens"]
                report.append("## Design Tokens")
                report.append(f"- Colors: {tokens['colors']}")
                report.append(f"- Typography tokens: {tokens['typography_tokens']}")
                report.append(f"- Spacing values: {tokens['spacing_values']}")
                report.append(f"- Effects shadows: {tokens['effects_shadows']}")
                report.append(f"- Effects blurs: {tokens['effects_blurs']}")
                report.append("")

            # Components summary
            if "components" in summary:
                components = summary["components"]
                report.append("## Components")
                report.append(f"- Total components: {components['total_components']}")
                report.append(f"- Components with variants: {components['with_variants']}")
                if components['by_category']:
                    report.append("- By category:")
                    for category, count in components['by_category'].items():
                        report.append(f"  - {category}: {count}")
                report.append("")

            # Layouts summary
            if "layouts" in summary:
                layouts = summary["layouts"]
                report.append("## Layouts")
                report.append(f"- Total screens: {layouts['total_screens']}")
                report.append(f"- Unique screen sizes: {layouts['screen_sizes']['unique_sizes']}")
                if layouts['layout_types']:
                    report.append("- Layout types:")
                    for layout_type, count in layouts['layout_types'].items():
                        report.append(f"  - {layout_type}: {count}")
                report.append("")

        return "\n".join(report)


def extract_from_figma_file(
    figma_file: 'figma_sdk.files.FigmaFile',
    output_dir: str = "extracted_assets",
    save_files: bool = True,
    validate: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to extract all assets from a Figma file.

    Args:
        figma_file: FigmaFile instance
        output_dir: Directory to save extracted assets
        save_files: Whether to save output files
        validate: Whether to validate outputs against schemas

    Returns:
        Dictionary containing all extraction results
    """
    extractor = DesignAssetExtractor(figma_file, output_dir)
    results = extractor.extract_all_assets()

    if save_files:
        extractor.save_outputs()

    if validate:
        validation_results = extractor.validate_outputs()
        results["validation"] = validation_results

    return results


def extract_from_file_key(
    file_key: str,
    project_name: str,
    access_token: str,
    output_dir: str = "extracted_assets",
    save_files: bool = True,
    validate: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to extract assets from Figma file key.

    Args:
        file_key: Figma file key
        project_name: Project name for caching
        access_token: Figma API access token
        output_dir: Directory to save extracted assets
        save_files: Whether to save output files
        validate: Whether to validate outputs against schemas

    Returns:
        Dictionary containing all extraction results
    """
    # Create Figma client and load file
    with figma_sdk.FigmaClient(token=access_token) as client:
        figma_file = figma_sdk.FigmaFile(file_key, project_name, client=client)
        return extract_from_figma_file(figma_file, output_dir, save_files, validate)