#!/usr/bin/env python3
"""
Manual component generator using templates
"""
import json
import os
from jinja2 import Environment, FileSystemLoader

def load_design_variables():
    """Load design variables for template usage"""
    try:
        with open('template_design_variables.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: design variables file not found")
        return {}

def load_component_config():
    """Load remaining component configuration"""
    with open('remaining_components_config.json', 'r') as f:
        config = json.load(f)
    return config

def render_component(component_name, component_config, design_vars):
    """Render a single component using the Figma-enhanced template"""
    env = Environment(loader=FileSystemLoader('templates'))

    # Prepare template context
    context = {
        'component_name': component_name.title(),
        'component_config': component_config,
        'design_vars': design_vars,
        'design_tokens': None  # We don't have Stage 2 design tokens loaded
    }

    # Load the Figma-enhanced template
    template = env.get_template('components/component_figma.j2')

    # Render the component
    rendered = template.render(**context)

    return rendered

def create_component_file(component_name, component_config, design_vars):
    """Create a component file"""
    # Determine the component category and file path
    category = component_config.get('category', 'display')

    # Map to proper directory structure
    if category == 'forms':
        dir_path = f'src/components/forms/{component_name}.tsx'
    elif category == 'navigation':
        dir_path = f'src/components/navigation/{component_name}.tsx'
    elif category == 'display':
        dir_path = f'src/components/display/{component_name}.tsx'
    else:
        dir_path = f'src/components/{component_name}.tsx'

    # Ensure directory exists
    os.makedirs(os.path.dirname(dir_path), exist_ok=True)

    # Render component
    rendered = render_component(component_name, component_config, design_vars)

    # Write to file
    with open(dir_path, 'w') as f:
        f.write(rendered)

    print(f"✅ Created {component_name} component at {dir_path}")
    return dir_path

def main():
    """Main function"""
    print("🔧 Manually generating components from remaining_components_config.json...")

    # Load design variables
    design_vars = load_design_variables()
    print(f"✅ Loaded design variables: {list(design_vars.keys())}")

    # Load component configuration
    config = load_component_config()
    components = config['interfaces']['components']

    print(f"📦 Found {len(components)} components to generate")

    # Generate each component
    for component_name, component_config in components.items():
        print(f"🔨 Generating {component_name}...")
        try:
            create_component_file(component_name, component_config, design_vars)
        except Exception as e:
            print(f"❌ Error generating {component_name}: {e}")

    print("✅ Component generation complete!")

if __name__ == "__main__":
    main()