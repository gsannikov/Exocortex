#!/usr/bin/env python3
"""
Centralized Configuration Loader for Claude Skill Template

This module provides a single source of truth for all repository configuration.
All scripts, tools, and documentation should use this to access configuration values.

Usage:
    from sdk.config.config_loader import TemplateConfig

    config = TemplateConfig()
    print(config.version)                    # "1.1.0"
    print(config.get('repository.owner'))    # "gsannikov"
    print(config.get_url('base'))            # Full GitHub URL
    print(config.get_path('skill_package'))  # "skill-package"
"""

import os
import yaml
from pathlib import Path
from typing import Any, Optional, Dict


class TemplateConfig:
    """
    Centralized configuration loader for the Claude Skill Template.

    Loads configuration from sdk/config/template-config.yaml and provides
    convenient access methods.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Optional path to config file. If None, auto-detects location.
        """
        if config_path is None:
            # Auto-detect config file location
            config_path = self._find_config_file()

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _find_config_file(self) -> str:
        """Find the template-config.yaml file in the repository."""
        # Try multiple possible locations
        possible_paths = [
            # From sdk/config/ (if script is in sdk/)
            Path(__file__).parent / "template-config.yaml",
            # From repository root
            Path(__file__).parent.parent.parent / "sdk/config/template-config.yaml",
            # Absolute path attempt
            Path.cwd() / "sdk/config/template-config.yaml",
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        raise FileNotFoundError(
            "Could not find template-config.yaml. Searched locations:\n" +
            "\n".join(f"  - {p}" for p in possible_paths)
        )

    def _load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {self.config_path}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key in dot notation (e.g., 'version.template')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config.get('version.template')
            '1.1.0'
            >>> config.get('repository.owner')
            'gsannikov'
            >>> config.get('paths.skill_package')
            'skill-package'
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    # =================================================================
    # CONVENIENCE PROPERTIES - Direct access to common values
    # =================================================================

    @property
    def version(self) -> str:
        """Get template version (e.g., '1.1.0')"""
        return self.get('version.template', 'unknown')

    @property
    def version_info(self) -> Dict[str, str]:
        """Get all version information"""
        return self.get('version', {})

    @property
    def repo_name(self) -> str:
        """Get repository name"""
        return self.get('repository.name', 'claude-skill-template')

    @property
    def repo_owner(self) -> str:
        """Get repository owner"""
        return self.get('repository.owner', 'gsannikov')

    @property
    def repo_description(self) -> str:
        """Get repository description"""
        return self.get('repository.description', '')

    @property
    def python_min_version(self) -> str:
        """Get minimum Python version"""
        return self.get('python.minimum_version', '3.8')

    @property
    def python_tested_version(self) -> str:
        """Get tested Python version"""
        return self.get('python.tested_version', '3.10')

    @property
    def storage_backends(self) -> list:
        """Get list of available storage backends"""
        return self.get('storage_backends.available', [])

    @property
    def storage_backend_count(self) -> int:
        """Get count of storage backends"""
        return self.get('storage_backends.count', 0)

    @property
    def test_count(self) -> int:
        """Get number of comprehensive tests"""
        return self.get('testing.comprehensive_test_count', 0)

    @property
    def license_type(self) -> str:
        """Get license type"""
        return self.get('license.type', 'MIT')

    # =================================================================
    # URL HELPERS
    # =================================================================

    def get_url(self, url_key: str) -> str:
        """
        Get URL by key.

        Args:
            url_key: URL key (e.g., 'base', 'issues', 'discussions')

        Returns:
            Full URL string

        Examples:
            >>> config.get_url('base')
            'https://github.com/gsannikov/claude-skill-template'
            >>> config.get_url('issues')
            'https://github.com/gsannikov/claude-skill-template/issues'
        """
        return self.get(f'urls.{url_key}', '')

    def get_clone_url(self, protocol: str = 'https') -> str:
        """
        Get clone URL for specified protocol.

        Args:
            protocol: 'https' or 'ssh'

        Returns:
            Clone URL
        """
        if protocol == 'ssh':
            return self.get_url('clone_ssh')
        return self.get_url('clone_https')

    # =================================================================
    # PATH HELPERS
    # =================================================================

    def get_path(self, path_key: str) -> str:
        """
        Get path by key.

        Args:
            path_key: Path key (e.g., 'skill_package', 'developer_tools')

        Returns:
            Path string

        Examples:
            >>> config.get_path('skill_package')
            'skill-package'
            >>> config.get_path('developer_tools')
            'developer-tools'
        """
        return self.get(f'paths.{path_key}', '')

    def get_full_path(self, path_key: str, relative_to: Optional[Path] = None) -> Path:
        """
        Get full path as Path object.

        Args:
            path_key: Path key from configuration
            relative_to: Base path (defaults to repository root)

        Returns:
            Full Path object
        """
        if relative_to is None:
            # Default to repository root (3 levels up from sdk/config/)
            relative_to = Path(__file__).parent.parent.parent

        rel_path = self.get_path(path_key)
        return relative_to / rel_path

    # =================================================================
    # DEPENDENCY HELPERS
    # =================================================================

    def get_dependency(self, dep_name: str) -> Dict[str, Any]:
        """
        Get dependency information.

        Args:
            dep_name: Dependency name (e.g., 'pyyaml', 'pygithub')

        Returns:
            Dictionary with dependency information
        """
        return self.get(f'dependencies.{dep_name}', {})

    def get_dependency_version(self, dep_name: str) -> str:
        """Get minimum version for a dependency"""
        return self.get(f'dependencies.{dep_name}.min_version', '')

    def get_pip_install_command(self, dep_name: str) -> str:
        """Get pip install command for a dependency"""
        return self.get(f'dependencies.{dep_name}.pip_install', f'{dep_name}')

    # =================================================================
    # STORAGE BACKEND HELPERS
    # =================================================================

    def get_storage_backend_display_name(self, backend: str) -> str:
        """
        Get display name for storage backend.

        Args:
            backend: Backend ID (e.g., 'local', 'github')

        Returns:
            Display name (e.g., 'Local Filesystem', 'GitHub')
        """
        return self.get(f'storage_backends.display_names.{backend}', backend.title())

    def get_storage_backend_description(self, backend: str) -> str:
        """Get description for storage backend"""
        return self.get(f'storage_backends.descriptions.{backend}', '')

    # =================================================================
    # TESTING HELPERS
    # =================================================================

    def get_test_names(self) -> list:
        """Get list of all test names"""
        return self.get('testing.test_names', [])

    def get_disabled_tests(self) -> list:
        """Get list of disabled tests"""
        return self.get('testing.disabled_tests', [])

    # =================================================================
    # GITHUB ACTIONS HELPERS
    # =================================================================

    def get_action_version(self, action_name: str) -> str:
        """
        Get GitHub Actions action version.

        Args:
            action_name: Action name (e.g., 'upload_artifact', 'checkout')

        Returns:
            Version string (e.g., 'v4', 'v3')
        """
        return self.get(f'github_actions.{action_name}_version', 'latest')

    # =================================================================
    # VALIDATION HELPERS
    # =================================================================

    def get_root_allowed_files(self) -> list:
        """Get list of files allowed in root folder"""
        return self.get('file_conventions.root_allowed', [])

    def get_root_forbidden_extensions(self) -> list:
        """Get list of forbidden extensions in root"""
        return self.get('file_conventions.root_forbidden_extensions', [])

    def get_session_patterns(self) -> list:
        """Get list of session/proposal file patterns"""
        return self.get('file_conventions.session_patterns', [])

    # =================================================================
    # UTILITY METHODS
    # =================================================================

    def reload(self):
        """Reload configuration from file"""
        self._load_config()

    def to_dict(self) -> Dict[str, Any]:
        """Get full configuration as dictionary"""
        return self._config.copy()

    def dump(self) -> str:
        """Dump configuration as YAML string"""
        return yaml.dump(self._config, default_flow_style=False, sort_keys=False)

    def __repr__(self) -> str:
        return f"TemplateConfig(version={self.version}, repo={self.repo_owner}/{self.repo_name})"


# =================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# =================================================================

_global_config: Optional[TemplateConfig] = None


def get_config() -> TemplateConfig:
    """Get global configuration instance (singleton pattern)"""
    global _global_config
    if _global_config is None:
        _global_config = TemplateConfig()
    return _global_config


def reload_config():
    """Reload global configuration"""
    global _global_config
    if _global_config is not None:
        _global_config.reload()
    else:
        _global_config = TemplateConfig()


# =================================================================
# CLI INTERFACE
# =================================================================

if __name__ == "__main__":
    """
    Command-line interface for configuration inspection.

    Usage:
        python sdk/config/config_loader.py
        python sdk/config/config_loader.py version
        python sdk/config/config_loader.py get version.template
    """
    import sys

    config = TemplateConfig()

    if len(sys.argv) == 1:
        # No arguments - show summary
        print("Claude Skill Template Configuration")
        print("=" * 50)
        print(f"Version: {config.version}")
        print(f"Repository: {config.repo_owner}/{config.repo_name}")
        print(f"Python: {config.python_min_version}+ (tested: {config.python_tested_version})")
        print(f"Storage Backends: {config.storage_backend_count}")
        print(f"Tests: {config.test_count}")
        print(f"License: {config.license_type}")
        print(f"\nConfig file: {config.config_path}")
        print(f"\nUsage: python {sys.argv[0]} get <key>")
        print(f"Example: python {sys.argv[0]} get version.template")

    elif len(sys.argv) == 2:
        # Single argument - treat as shortcut property
        arg = sys.argv[1]
        if hasattr(config, arg):
            print(getattr(config, arg))
        else:
            print(f"Error: Unknown property '{arg}'")
            sys.exit(1)

    elif len(sys.argv) >= 3 and sys.argv[1] == "get":
        # Get specific key
        key = sys.argv[2]
        value = config.get(key)
        if value is None:
            print(f"Error: Key '{key}' not found")
            sys.exit(1)
        else:
            if isinstance(value, (dict, list)):
                print(yaml.dump(value, default_flow_style=False))
            else:
                print(value)

    else:
        print(f"Usage: python {sys.argv[0]} [get] <key>")
        sys.exit(1)
