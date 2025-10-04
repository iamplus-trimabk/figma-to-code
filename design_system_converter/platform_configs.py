"""
Platform Configs - Manages platform-specific configurations and optimizations.

Handles web (Tailwind CSS), mobile (NativeWind), and cross-platform configurations
with platform-specific optimizations.
"""

from typing import Dict, List, Any, Optional
from .schemas import (
    PlatformType, PlatformConfig, TailwindTheme, NativeWindTheme,
    DesignTokens, ConversionOutput
)


class PlatformConfigs:
    """Manages platform-specific configurations and optimizations."""

    def __init__(self):
        self.web_optimizations = {
            'purge': True,
            'minify': True,
            'autoprefixer': True,
            'css_variables': True,
            'critical_css': True
        }

        self.mobile_optimizations = {
            'tree_shaking': True,
            'bundle_optimization': True,
            'font_optimization': True,
            'image_optimization': True,
            'lazy_loading': True
        }

    def get_web_config(self, tailwind_theme: TailwindTheme, design_tokens: DesignTokens) -> PlatformConfig:
        """Get web platform configuration (Tailwind CSS)."""
        config = {
            'theme': tailwind_theme.to_dict(),
            'plugins': self._get_web_plugins(),
            'content': self._get_web_content_paths(),
            'presets': self._get_web_presets()
        }

        optimizations = {
            'purge': {
                'enabled': self.web_optimizations['purge'],
                'content': self._get_web_content_paths(),
                'options': {
                    'safelist': self._get_web_safelist()
                }
            },
            'corePlugins': self._get_web_core_plugins(),
            'darkMode': self._get_web_dark_mode_config(),
            'variants': self._get_web_variants(),
            'cssVariables': self.web_optimizations['css_variables']
        }

        return PlatformConfig(
            platform=PlatformType.WEB,
            config=config,
            optimizations=optimizations
        )

    def get_mobile_config(self, native_wind_theme: NativeWindTheme, design_tokens: DesignTokens) -> PlatformConfig:
        """Get mobile platform configuration (NativeWind)."""
        config = {
            'theme': native_wind_theme.to_dict(),
            'plugins': self._get_mobile_plugins(),
            'project': self._get_mobile_project_config(),
            'output': self._get_mobile_output_config()
        }

        optimizations = {
            'treeShaking': self.mobile_optimizations['tree_shaking'],
            'bundleOptimization': self.mobile_optimizations['bundle_optimization'],
            'fontOptimization': self.mobile_optimizations['font_optimization'],
            'imageOptimization': self.mobile_optimizations['image_optimization'],
            'lazyLoading': self.mobile_optimizations['lazy_loading']
        }

        return PlatformConfig(
            platform=PlatformType.MOBILE,
            config=config,
            optimizations=optimizations
        )

    def generate_shared_config(self, design_tokens: DesignTokens) -> Dict[str, Any]:
        """Generate shared configuration for cross-platform usage."""
        shared_config = {
            'tokens': {
                'colors': design_tokens.colors.to_dict(),
                'typography': design_tokens.typography.to_dict(),
                'spacing': design_tokens.spacing.to_dict(),
                'effects': design_tokens.effects.to_dict()
            },
            'breakpoints': self._get_shared_breakpoints(),
            'container': self._get_shared_container_config(),
            'animations': self._get_shared_animations(),
            'transitions': self._get_shared_transitions()
        }

        return shared_config

    def optimize_for_platform(self, platform: PlatformType, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply platform-specific optimizations."""
        if platform == PlatformType.WEB:
            return self._optimize_web_config(config)
        elif platform == PlatformType.MOBILE:
            return self._optimize_mobile_config(config)
        else:
            return config

    def _get_web_plugins(self) -> List[str]:
        """Get Tailwind CSS plugins for web platform."""
        return [
            '@tailwindcss/forms',
            '@tailwindcss/typography',
            '@tailwindcss/aspect-ratio',
            '@tailwindcss/container-queries'
        ]

    def _get_web_content_paths(self) -> List[str]:
        """Get content paths for Tailwind CSS purging."""
        return [
            './src/**/*.{js,ts,jsx,tsx}',
            './pages/**/*.{js,ts,jsx,tsx}',
            './components/**/*.{js,ts,jsx,tsx}',
            './app/**/*.{js,ts,jsx,tsx}'
        ]

    def _get_web_presets(self) -> List[str]:
        """Get Tailwind CSS presets."""
        return [
            'default'
        ]

    def _get_web_safelist(self) -> List[str]:
        """Get safelist for Tailwind CSS purging."""
        return [
            'bg-primary',
            'bg-secondary',
            'text-primary',
            'text-secondary',
            'border-primary',
            'hover:bg-primary-dark',
            'focus:bg-primary-light',
            # Dynamic values that shouldn't be purged
            r'/^bg-/',
            r'/^text-/',
            r'/^border-/',
            r'/^p-/',
            r'/^m-/',
            r'/^w-/',
            r'/^h-/'
        ]

    def _get_web_core_plugins(self) -> Dict[str, bool]:
        """Get core plugins configuration for web."""
        return {
            'float': True,
            'clear': True,
            'overflow': True,
            'display': True,
            'position': True,
            'top': True,
            'right': True,
            'bottom': True,
            'left': True,
            'inset': True,
            'isolation': True,
            'zIndex': True,
            'flex': True,
            'flexDirection': True,
            'flexWrap': True,
            'flexGrow': True,
            'flexShrink': True,
            'flexBasis': True,
            'grid': True,
            'gridTemplateColumns': True,
            'gridTemplateRows': True,
            'gridTemplateAreas': True,
            'gridAutoColumns': True,
            'gridAutoRows': True,
            'gridAutoFlow': True,
            'gap': True,
            'space': True,
            'divideColor': True,
            'divideStyle': True,
            'divideWidth': True,
            'divideX': True,
            'divideY': True,
            'placeSelf': True,
            'placeItems': True,
            'placeContent': True,
            'alignContent': True,
            'alignItems': True,
            'alignSelf': True,
            'justifyContent': True,
            'justifyItems': True,
            'justifySelf': True,
            'padding': True,
            'margin': True,
            'width': True,
            'minWidth': True,
            'maxWidth': True,
            'height': True,
            'minHeight': True,
            'maxHeight': True,
            'fontSize': True,
            'fontSmoothing': True,
            'fontStyle': True,
            'fontWeight': True,
            'fontVariantNumeric': True,
            'fontFamily': True,
            'lineHeight': True,
            'letterSpacing': True,
            'textColor': True,
            'textDecoration': True,
            'textIndent': True,
            'textOpacity': True,
            'textOverflow': True,
            'textTransform': True,
            'verticalAlign': True,
            'whitespace': True,
            'wordBreak': True,
            'backgroundColor': True,
            'backgroundOpacity': True,
            'backgroundPosition': True,
            'backgroundSize': True,
            'borderColor': True,
            'borderOpacity': True,
            'borderStyle': True,
            'borderWidth': True,
            'borderTopWidth': True,
            'borderRightWidth': True,
            'borderBottomWidth': True,
            'borderLeftWidth': True,
            'borderRadius': True,
            'boxShadow': True,
            'boxSizing': True,
            'cursor': True,
            'transform': True,
            'transformOrigin': True,
            'transition': True,
            'transitionDelay': True,
            'transitionDuration': True,
            'transitionProperty': True,
            'transitionTimingFunction': True,
            'animation': True,
            'animationDelay': True,
            'animationDirection': True,
            'animationDuration': True,
            'animationFillMode': True,
            'animationIterationCount': True,
            'animationName': True,
            'animationPlayState': True,
            'animationTimingFunction': True,
            'opacity': True,
            'objectFit': True,
            'objectPosition': True
        }

    def _get_web_dark_mode_config(self) -> Dict[str, Any]:
        """Get dark mode configuration for web."""
        return {
            'media': '(prefers-color-scheme: dark)',
            'classSelector': '.dark',
            'classPrefix': 'dark:',
            'variantPrefix': 'dark:'
        }

    def _get_web_variants(self) -> Dict[str, List[str]]:
        """Get variant configuration for web."""
        return {
            'responsive': ['sm', 'md', 'lg', 'xl', '2xl'],
            'hover': ['hover'],
            'focus': ['focus'],
            'active': ['active'],
            'disabled': ['disabled'],
            'group-hover': ['group-hover'],
            'group-focus': ['group-focus'],
            'dark': ['dark'],
            'motion-safe': ['motion-safe'],
            'motion-reduce': ['motion-reduce'],
            'first': ['first'],
            'last': ['last'],
            'odd': ['odd'],
            'even': ['even'],
            'visited': ['visited'],
            'checked': ['checked']
        }

    def _get_mobile_plugins(self) -> List[str]:
        """Get NativeWind plugins for mobile platform."""
        return [
            'nativewind/plugin',
            '@nativewind/plugin'
        ]

    def _get_mobile_project_config(self) -> Dict[str, Any]:
        """Get NativeWind project configuration."""
        return {
            'ios': {
                'shadowColor': True,
                'shadowOffset': True,
                'shadowOpacity': True,
                'shadowRadius': True,
                'elevation': True,
                'zIndex': True
            },
            'android': {
                'elevation': True,
                'zIndex': True
            },
            'web': {
                'shadowColor': True,
                'shadowOffset': True,
                'shadowOpacity': True,
                'shadowRadius': True,
                'elevation': True,
                'zIndex': True
            }
        }

    def _get_mobile_output_config(self) -> Dict[str, Any]:
        """Get NativeWind output configuration."""
        return {
            'native': True,
            'web': True,
            'inlineRem': True,
            'output': {
                'css': './styles/nativewind.css',
                'js': './styles/nativewind.js'
            }
        }

    def _get_shared_breakpoints(self) -> Dict[str, Any]:
        """Get shared breakpoint configuration."""
        return {
            'sm': '640px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1280px',
            '2xl': '1536px'
        }

    def _get_shared_container_config(self) -> Dict[str, Any]:
        """Get shared container configuration."""
        return {
            'center': True,
            'padding': '2rem',
            'screens': {
                '2xl': '1400px'
            }
        }

    def _get_shared_animations(self) -> Dict[str, str]:
        """Get shared animation definitions."""
        return {
            'spin': 'spin 1s linear infinite',
            'ping': 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
            'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            'bounce': 'bounce 1s infinite'
        }

    def _get_shared_transitions(self) -> Dict[str, Any]:
        """Get shared transition configuration."""
        return {
            'property': 'all',
            'timingFunction': 'cubic-bezier(0.4, 0, 0.2, 1)',
            'duration': '150ms'
        }

    def _optimize_web_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply web-specific optimizations."""
        optimized_config = config.copy()

        # Add optimization settings
        if 'optimizations' not in optimized_config:
            optimized_config['optimizations'] = {}

        optimized_config['optimizations'].update({
            'purgeCSS': True,
            'minifyCSS': True,
            'autoprefixer': True,
            'criticalCSS': True,
            'fontDisplay': 'swap',
            'imageOptimization': True,
            'lazyLoading': True
        })

        # Web-specific performance settings
        optimized_config['performance'] = {
            'unusedClassesRemoval': True,
            'cssNesting': True,
            'cssCustomProperties': True,
            'containerQueries': True
        }

        return optimized_config

    def _optimize_mobile_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply mobile-specific optimizations."""
        optimized_config = config.copy()

        # Add optimization settings
        if 'optimizations' not in optimized_config:
            optimized_config['optimizations'] = {}

        optimized_config['optimizations'].update({
            'treeShaking': True,
            'bundleOptimization': True,
            'fontOptimization': True,
            'imageOptimization': True,
            'lazyLoading': True,
            'memoryOptimization': True
        })

        # Mobile-specific performance settings
        optimized_config['performance'] = {
            'runtimeOptimization': True,
            'memoryUsage': 'low',
            'bundleSize': 'minimal',
            'renderOptimization': True
        }

        # Platform-specific optimizations
        optimized_config['platformSpecific'] = {
            'ios': {
                'shadowPerformance': True,
                'animationPerformance': True,
                'memoryEfficiency': True
            },
            'android': {
                'shadowPerformance': True,
                'animationPerformance': True,
                'memoryEfficiency': True
            },
            'web': {
                'cssPerformance': True,
                'animationPerformance': True,
                'loadPerformance': True
            }
        }

        return optimized_config

    def generate_platform_specific_configs(self, design_tokens: DesignTokens,
                                         tailwind_theme: TailwindTheme,
                                         native_wind_theme: NativeWindTheme) -> List[PlatformConfig]:
        """Generate all platform-specific configurations."""
        configs = []

        # Web configuration
        web_config = self.get_web_config(tailwind_theme, design_tokens)
        configs.append(web_config)

        # Mobile configuration
        mobile_config = self.get_mobile_config(native_wind_theme, design_tokens)
        configs.append(mobile_config)

        # Apply optimizations
        for config in configs:
            config.config = self.optimize_for_platform(config.platform, config.config)

        return configs

    def export_configs(self, configs: List[PlatformConfig], output_dir: str) -> Dict[str, str]:
        """Export configurations to files."""
        exported_files = {}

        for config in configs:
            filename = f"{config.platform.value}_config.json"
            filepath = f"{output_dir}/{filename}"

            # In a real implementation, this would write to file
            # For now, return the export paths
            exported_files[config.platform.value] = filepath

        return exported_files