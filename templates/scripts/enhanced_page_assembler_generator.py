#!/usr/bin/env python3
"""
Enhanced Page Assembler Generator

Generates complete pages from Figma layouts using enhanced component generation
with our learnings from manual fixes applied.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple
from component_generator import ComponentGenerator


class EnhancedPageAssemblerGenerator:
    """Enhanced page assembler that generates complete pages with proper styling"""

    def __init__(self, stage2_outputs_path: str, templates_dir: str, output_dir: str):
        self.stage2_outputs_path = Path(stage2_outputs_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.stage2_outputs = self._load_stage2_outputs()
        self.component_generator = ComponentGenerator(stage2_outputs_path, templates_dir, output_dir)

    def _load_stage2_outputs(self) -> Dict[str, Any]:
        """Load Stage 2 outputs"""
        if not self.stage2_outputs_path.exists():
            raise FileNotFoundError(f"Stage 2 outputs not found: {self.stage2_outputs_path}")

        if self.stage2_outputs_path.is_dir():
            outputs = {}
            for json_file in self.stage2_outputs_path.glob("*.json"):
                with open(json_file, 'r') as f:
                    outputs[json_file.name] = json.load(f)
            return outputs
        else:
            with open(self.stage2_outputs_path, 'r') as f:
                return json.load(f)

    def _get_screen_layouts(self) -> Dict[str, Any]:
        """Get screen layouts from stage 2 outputs"""
        for key, value in self.stage2_outputs.items():
            if key == 'screen_layouts.json':
                return value
            elif isinstance(value, dict) and 'screen_layouts' in value:
                return value['screen_layouts']
        return {}

    def _get_component_catalog(self) -> List[Dict[str, Any]]:
        """Get component catalog from stage 2 outputs"""
        for key, value in self.stage2_outputs.items():
            if key == 'component_catalog.json':
                return value.get('components', [])
            elif isinstance(value, dict) and 'component_catalog' in value:
                return value['component_catalog'].get('components', [])
        return []

    def _analyze_component_type(self, component_name: str, component_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze component type and determine how to render it"""
        name_lower = component_name.lower()

        # Social login buttons
        if 'google' in name_lower:
            return {
                'type': 'social_button',
                'variant': 'google',
                'text': 'Continue with Google',
                'props': {
                    'className': 'w-full flex items-center justify-center gap-2 border border-gray-200 bg-white hover:bg-gray-50 text-black rounded-lg',
                    'style': 'padding: 12px 16px; fontSize: 16px; fontWeight: 500;'
                }
            }
        elif 'facebook' in name_lower:
            return {
                'type': 'social_button',
                'variant': 'facebook',
                'text': 'Continue with Facebook',
                'props': {
                    'className': 'w-full flex items-center justify-center gap-2 border border-blue-600 bg-blue-600 hover:bg-blue-700 text-white rounded-lg',
                    'style': 'padding: 12px 16px; fontSize: 16px; fontWeight: 500;'
                }
            }

        # Primary action buttons
        elif 'login' in name_lower or 'sign in' in name_lower or name_lower == 'button':
            return {
                'type': 'primary_button',
                'variant': 'primary',
                'text': 'Login',
                'props': {
                    'className': 'w-full bg-primary-500 text-white hover:bg-primary-600 rounded-lg',
                    'style': 'padding: 12px 24px; fontSize: 16px; fontWeight: 500; backgroundColor: #6257db;'
                }
            }

        # Input fields
        elif 'email' in name_lower:
            return {
                'type': 'input',
                'input_type': 'email',
                'props': {
                    'placeholder': 'Enter your email',
                    'className': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                    'style': 'padding: 12px 16px; fontSize: 16px;'
                }
            }
        elif 'password' in name_lower:
            return {
                'type': 'input',
                'input_type': 'password',
                'props': {
                    'placeholder': 'Enter your password',
                    'className': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                    'style': 'padding: 12px 16px; fontSize: 16px;'
                }
            }

        # Text components
        elif 'welcome' in name_lower or 'design school' in name_lower:
            return {
                'type': 'heading',
                'level': 'h1',
                'text': 'Welcome to Design School',
                'props': {
                    'className': 'text-2xl font-bold text-gray-900 mb-6',
                    'style': 'fontSize: 2rem; fontWeight: bold; color: #2e2e2e; textAlign: left; backgroundColor: transparent;'
                }
            }
        elif 'or' == name_lower:
            return {
                'type': 'text',
                'text': 'or',
                'props': {
                    'className': 'text-gray-600 text-center my-4',
                    'style': 'fontSize: 1rem; color: #6b7280; textAlign: center;'
                }
            }
        elif 'remember' in name_lower:
            return {
                'type': 'checkbox',
                'text': 'Remember me',
                'props': {
                    'className': 'flex items-center justify-start w-full',
                    'style': 'textAlign: left; alignSelf: flex-start;'
                }
            }
        elif 'forgot password' in name_lower:
            return {
                'type': 'link',
                'text': 'Forgot Password?',
                'props': {
                    'className': 'text-primary underline text-sm justify-self-end',
                    'style': 'color: #6257db; textDecoration: underline; fontSize: 14px; textAlign: right;'
                }
            }
        elif 'register' in name_lower or "don't have" in name_lower:
            return {
                'type': 'text',
                'text': "Don't have an account? Register",
                'props': {
                    'className': 'text-sm text-gray-600 text-left',
                    'style': 'fontSize: 0.875rem; color: #000000; textAlign: left; backgroundColor: transparent;'
                }
            }

        # Background cards
        elif name_lower == 'bg':
            return {
                'type': 'container',
                'props': {
                    'className': 'bg-white rounded-lg shadow-lg p-8',
                    'style': 'backgroundColor: #ffffff; borderRadius: 8px; padding: 2rem; boxShadow: 0 4px 6px rgba(0, 0, 0, 0.1);'
                }
            }

        # Illustration/placeholder
        elif 'illustration' in name_lower:
            return {
                'type': 'placeholder',
                'text': 'Illustration',
                'props': {
                    'className': 'bg-gray-100 rounded-lg p-8 flex items-center justify-center',
                    'style': 'backgroundColor: #f0f0f0; borderRadius: 8px; minHeight: 400px;'
                }
            }

        # Default
        else:
            return {
                'type': 'text',
                'text': component_name,
                'props': {
                    'className': 'text-gray-900',
                    'style': 'color: #374151;'
                }
            }

    def _generate_login_page(self, screen_name: str, screen_data: Dict[str, Any]) -> str:
        """Generate a complete login page from screen data"""

        # Analyze components
        children = screen_data.get('children', [])
        analyzed_components = []

        for child in children:
            component_analysis = self._analyze_component_type(child['name'], child)
            analyzed_components.append(component_analysis)

        # Generate React component code
        component_code = f'''/**
 * Login Page - Generated by Enhanced Page Assembler
 *
 * Automatically generated from Figma screen: {screen_name}
 * Uses enhanced component generation with proper styling and layout
 */

"use client"

import React from "react"
import {{ Button }} from "@/components/navigation/button"
import {{ Input }} from "@/components/forms/input"
import {{ Card }} from "@/components/display/card"

export default function LoginPage() {{
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="w-full h-full">
        <div className="flex flex-row items-center justify-center w-full min-h-screen bg-gray-50 p-8 gap-8">
          {{/* Illustration Side */}}
          <div className="flex-1 max-w-2xl flex items-center justify-center">
            <div className="bg-gray-100 rounded-lg p-8 flex items-center justify-center" style={{{{ minHeight: '400px', backgroundColor: '#f0f0f0', borderRadius: '8px' }}}}>
              <span className="text-gray-600 text-lg">Illustration</span>
            </div>
          </div>

          {{/* Form Card Side */}}
          <div className="flex-1 max-w-md w-full">
            <div className="bg-white rounded-lg shadow-lg p-8" style={{{{ backgroundColor: '#ffffff', borderRadius: '8px', padding: '2rem', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)' }}}}>
              <div className="flex flex-col items-stretch space-y-4">
'''

        # Add components to the page
        for component in analyzed_components:
            if component['type'] == 'heading':
                component_code += f'''
                <h1 className="text-2xl font-bold text-gray-900 mb-6" style={{{{ fontSize: '2rem', fontWeight: 'bold', color: '#2e2e2e', textAlign: 'left', backgroundColor: 'transparent' }}}}>
                  {component['text']}
                </h1>'''

            elif component['type'] == 'social_button':
                component_code += f'''
                <Button
                  variant="{component['variant']}"
                  className="w-full flex items-center justify-center gap-2 border rounded-lg"
                  style={{{{ padding: '12px 16px', fontSize: '16px', fontWeight: '500' }}}}
                >
                  {component['text']}
                </Button>'''

            elif component['type'] == 'text' and component['text'] == 'or':
                component_code += f'''
                <div className="text-gray-600 text-center my-4" style={{{{ fontSize: '1rem', color: '#6b7280', textAlign: 'center' }}}}>
                  {component['text']}
                </div>'''

            elif component['type'] == 'input':
                input_type = component.get('input_type', 'text')
                placeholder = component['props']['placeholder']
                component_code += f'''
                <Input
                  type="{input_type}"
                  placeholder="{placeholder}"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  style={{{{ padding: '12px 16px', fontSize: '16px' }}}}
                />'''

            elif component['type'] == 'primary_button':
                component_code += f'''
                <Button
                  variant="primary"
                  className="w-full bg-primary-500 text-white hover:bg-primary-600 rounded-lg"
                  style={{{{ backgroundColor: '#6257db', padding: '12px 24px', fontSize: '16px', fontWeight: '500' }}}}
                  type="submit"
                >
                  {component['text']}
                </Button>'''

            elif component['type'] == 'checkbox':
                component_code += f'''
                <div className="flex items-center space-x-2 text-sm text-gray-600" style={{{{ textAlign: 'left', alignSelf: 'flex-start' }}}}>
                  <input type="checkbox" className="rounded border-gray-300" />
                  <span>{component['text']}</span>
                </div>'''

            elif component['type'] == 'link':
                component_code += f'''
                <button
                  className="text-primary underline text-sm"
                  style={{{{ color: '#6257db', textDecoration: 'underline', fontSize: '14px', textAlign: 'right' }}}}
                >
                  {component['text']}
                </button>'''

            elif component['type'] == 'text' and 'register' in component['text'].lower():
                component_code += f'''
                <div className="text-sm text-gray-600 text-left mt-4" style={{{{ fontSize: '0.875rem', color: '#000000', textAlign: 'left', backgroundColor: 'transparent' }}}}>
                  {component['text']}
                </div>'''

        component_code += '''
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}'''

        return component_code

    def generate_login_page(self) -> str:
        """Generate an enhanced login page"""
        print("Generating enhanced login page from Figma layouts...")

        # Get screen layouts
        screen_layouts = self._get_screen_layouts()
        if not screen_layouts:
            raise ValueError("No screen layouts found in Stage 2 outputs")

        # Find login screen
        login_screen = None
        screens = screen_layouts.get('screens', [])
        for screen in screens:
            if screen.get('name', '').lower() == 'login':
                login_screen = screen
                break

        if not login_screen:
            raise ValueError("Login screen not found in screen layouts")

        # Generate login page
        login_page_code = self._generate_login_page('Login', login_screen)

        # Save the login page
        login_page_dir = self.output_dir / "src" / "app" / "generated-login"
        login_page_dir.mkdir(parents=True, exist_ok=True)

        page_file = login_page_dir / "page.tsx"
        with open(page_file, 'w') as f:
            f.write(login_page_code)

        print(f"Generated enhanced login page: {page_file}")
        return login_page_code

    def generate_all_pages(self):
        """Generate all pages from screen layouts"""
        print("Generating all pages from Figma layouts...")

        screen_layouts = self._get_screen_layouts()
        if not screen_layouts:
            print("No screen layouts found")
            return []

        screens = screen_layouts.get('screens', [])
        generated_pages = []

        for screen in screens:
            screen_name = screen.get('name', 'Unknown')
            try:
                if screen_name.lower() == 'login':
                    page_code = self._generate_login_page(screen_name, screen)

                    # Save page
                    page_dir = self.output_dir / "src" / "app" / f"{screen_name.lower().replace(' ', '-')}"
                    page_dir.mkdir(parents=True, exist_ok=True)

                    page_file = page_dir / "page.tsx"
                    with open(page_file, 'w') as f:
                        f.write(page_code)

                    generated_pages.append({
                        'name': screen_name,
                        'path': str(page_file),
                        'type': 'login'
                    })

                    print(f"Generated page: {screen_name} -> {page_file}")

            except Exception as e:
                print(f"Failed to generate page {screen_name}: {e}")
                continue

        return generated_pages


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate enhanced pages from Figma layouts')
    parser.add_argument('--stage2', required=True, help='Path to Stage 2 outputs directory')
    parser.add_argument('--templates', default='templates', help='Path to templates directory')
    parser.add_argument('--output', default='.', help='Output directory')
    parser.add_argument('--login-only', action='store_true', help='Generate only login page')

    args = parser.parse_args()

    try:
        generator = EnhancedPageAssemblerGenerator(args.stage2, args.templates, args.output)

        if args.login_only:
            generator.generate_login_page()
        else:
            pages = generator.generate_all_pages()
            print(f"\nGenerated {len(pages)} pages")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())