"""
JSON schema definitions for design asset extraction outputs.

Defines the structure and validation rules for all extracted data
to ensure consistency and compatibility with downstream stages.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json


@dataclass
class ColorToken:
    """Design token for colors."""
    name: str
    value: str
    type: str  # solid, gradient, semantic
    description: Optional[str] = None


@dataclass
class TypographyToken:
    """Design token for typography."""
    name: str
    font_family: str
    font_size: float
    font_weight: int
    line_height: float
    letter_spacing: Optional[float] = None
    description: Optional[str] = None


@dataclass
class SpacingToken:
    """Design token for spacing."""
    name: str
    value: float
    unit: str = "px"
    description: Optional[str] = None


@dataclass
class ComponentVariant:
    """Component variant definition."""
    name: str
    props: Dict[str, Any]
    example_usage: Optional[str] = None


@dataclass
class ComponentSpec:
    """Component specification."""
    name: str
    type: str  # interactive, display, layout, text
    props: Dict[str, Any]
    variants: List[ComponentVariant]
    children: List[Dict[str, Any]]
    description: Optional[str] = None


@dataclass
class ScreenLayout:
    """Screen layout specification."""
    name: str
    type: str
    size: Dict[str, float]
    background_color: Optional[str] = None
    children: List[Dict[str, Any]] = None
    layout: Dict[str, Any] = None
    description: Optional[str] = None


class DesignAssetSchemas:
    """JSON schema definitions for output validation."""

    @staticmethod
    def design_tokens_schema() -> Dict[str, Any]:
        """Schema for design tokens output."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "colors": {
                    "type": "object",
                    "properties": {
                        "semantic": {
                            "type": "object",
                            "patternProperties": {
                                "^[a-z][a-z0-9-]*$": {
                                    "type": "string",
                                    "pattern": "^#[0-9a-fA-F]{6}$"
                                }
                            }
                        },
                        "neutral": {
                            "type": "object",
                            "patternProperties": {
                                "^[a-z][a-z0-9-]*$": {
                                    "type": "string",
                                    "pattern": "^#[0-9a-fA-F]{6}$"
                                }
                            }
                        },
                        "brand": {
                            "type": "object",
                            "patternProperties": {
                                "^[a-z][a-z0-9-]*$": {
                                    "type": "string",
                                    "pattern": "^#[0-9a-fA-F]{6}$"
                                }
                            }
                        }
                    }
                },
                "typography": {
                    "type": "object",
                    "properties": {
                        "fontFamily": {"type": "string"},
                        "fontSizes": {
                            "type": "object",
                            "patternProperties": {
                                "^[a-z][a-z0-9-]*$": {"type": "number"}
                            }
                        },
                        "fontWeights": {
                            "type": "object",
                            "patternProperties": {
                                "^[a-z][a-z0-9-]*$": {"type": "number"}
                            }
                        },
                        "lineHeights": {
                            "type": "object",
                            "patternProperties": {
                                "^[a-z][a-z0-9-]*$": {"type": "number"}
                            }
                        }
                    },
                    "required": ["fontFamily"]
                },
                "spacing": {
                    "type": "object",
                    "patternProperties": {
                        "^[a-z][a-z0-9-]*$": {"type": "number"}
                    }
                },
                "effects": {
                    "type": "object",
                    "properties": {
                        "shadows": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "value": {"type": "string"}
                                }
                            }
                        },
                        "blurs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "value": {"type": "number"}
                                }
                            }
                        }
                    }
                }
            },
            "required": ["colors", "typography"]
        }

    @staticmethod
    def component_catalog_schema() -> Dict[str, Any]:
        """Schema for component catalog output."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "components": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["interactive", "display", "layout", "text"]
                            },
                            "category": {"type": "string"},
                            "props": {"type": "object"},
                            "variants": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "props": {"type": "object"},
                                        "example_usage": {"type": "string"}
                                    }
                                }
                            },
                            "children": {
                                "type": "array",
                                "items": {"type": "object"}
                            },
                            "description": {"type": "string"}
                        },
                        "required": ["name", "type", "props"]
                    }
                }
            },
            "required": ["components"]
        }

    @staticmethod
    def screen_layouts_schema() -> Dict[str, Any]:
        """Schema for screen layouts output."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "screens": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "size": {
                                "type": "object",
                                "properties": {
                                    "width": {"type": "number"},
                                    "height": {"type": "number"}
                                }
                            },
                            "background_color": {"type": "string"},
                            "children": {
                                "type": "array",
                                "items": {"type": "object"}
                            },
                            "layout": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string"},
                                    "direction": {"type": "string"},
                                    "spacing": {"type": "number"}
                                }
                            },
                            "description": {"type": "string"}
                        },
                        "required": ["name", "type", "size"]
                    }
                }
            },
            "required": ["screens"]
        }

    @staticmethod
    def validate_output(data: Dict[str, Any], schema_type: str) -> bool:
        """Validate output data against schema."""
        try:
            if schema_type == "design_tokens":
                schema = DesignAssetSchemas.design_tokens_schema()
            elif schema_type == "component_catalog":
                schema = DesignAssetSchemas.component_catalog_schema()
            elif schema_type == "screen_layouts":
                schema = DesignAssetSchemas.screen_layouts_schema()
            else:
                raise ValueError(f"Unknown schema type: {schema_type}")

            # Simple validation - in production, use jsonschema library
            required_keys = schema.get("required", [])
            for key in required_keys:
                if key not in data:
                    print(f"Missing required key: {key}")
                    return False

            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False