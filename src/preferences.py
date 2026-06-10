"""
Preferences Manager for OAS Generation Tool.
Handles loading, saving, and providing default values for user preferences.
"""

import os
import json
from copy import deepcopy
from pathlib import Path


GENERATION_MODE_MINIMAL = "Minimal"
GENERATION_MODE_STANDARD = "Standard"
GENERATION_MODE_API_PORTAL_READY = "API Portal-ready"
GENERATION_MODES = (
    GENERATION_MODE_MINIMAL,
    GENERATION_MODE_STANDARD,
    GENERATION_MODE_API_PORTAL_READY,
)
DEFAULT_GENERATION_MODE = GENERATION_MODE_API_PORTAL_READY
LEGACY_GITHUB_PAGES_UPDATE_MANIFEST_URL = "https://cernutog.github.io/oasis/oasis-version.json"
DEFAULT_UPDATE_MANIFEST_URL = "https://raw.githubusercontent.com/cernutog/oasis/gh-pages/oasis-version.json"
X_INFO_EXTENSION_OPTION_KEYS = {
    "creation_date": "gen_x_info_creation_date",
    "release": "gen_x_info_release",
    "customization": "gen_x_info_customization",
    "oasis_version": "gen_x_info_oasis_version",
}
DEFAULT_X_INFO_OPTIONS = {name: True for name in X_INFO_EXTENSION_OPTION_KEYS}
DEFAULT_SWIFT_SERVICES = {
    "B2B": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/b2b/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/b2b/v1",
                "description": "Test Environment",
            },
        ]
    },
    "CGS": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/cgs/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/cgs/v1",
                "description": "Test Environment",
            },
        ]
    },
    "CGS-DKK": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/cgs-dkk/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/cgs-dkk/v1",
                "description": "Test Environment",
            },
        ]
    },
    "COR": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/cor/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/cor/v1",
                "description": "Test Environment",
            },
        ]
    },
    "DCT": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/dct/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/dct/v1",
                "description": "Test Environment",
            },
        ]
    },
    "FPAD": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/fpad/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/fpad/v1",
                "description": "Test Environment",
            },
        ]
    },
    "R2P": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/r2p/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/r2p/v1",
                "description": "Test Environment",
            },
        ]
    },
    "RT1": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/rt1/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/rt1/v1",
                "description": "Test Environment",
            },
        ]
    },
    "SCT": {
        "servers": [
            {
                "url": "https://ebaclapi.swiftnet.sipn.swift.com/sct/v1",
                "description": "Live Environment",
            },
            {
                "url": "https://ebaclapi-pilot.swiftnet.sipn.swift.com/sct/v1",
                "description": "Test Environment",
            },
        ]
    },
}


def normalize_update_manifest_url(value) -> str:
    text = str(value or "").strip()
    if text == LEGACY_GITHUB_PAGES_UPDATE_MANIFEST_URL:
        return DEFAULT_UPDATE_MANIFEST_URL
    return text


def migrate_saved_preferences(saved: dict) -> dict:
    migrated = dict(saved)

    # Migration Logic: template_directory -> excel_input_folder
    if "template_directory" in migrated and not migrated.get("excel_input_folder"):
        migrated["excel_input_folder"] = migrated["template_directory"]

    if "update_manifest_url" in migrated:
        migrated["update_manifest_url"] = normalize_update_manifest_url(migrated.get("update_manifest_url"))

    return migrated


def validate_preference_value(key: str, value):
    if key not in PreferencesManager.DEFAULT_PREFERENCES:
        return False, value, "unknown preference"

    default = PreferencesManager.DEFAULT_PREFERENCES[key]
    if key == "generation_mode":
        text = str(value or "").strip()
        for mode in GENERATION_MODES:
            if text.lower() == mode.lower():
                return True, mode, ""
        return False, value, "expected supported generation mode"
    if key == "update_manifest_url":
        return True, normalize_update_manifest_url(value), ""

    if default is None:
        if value is None or isinstance(value, str):
            return True, value, ""
        return False, value, "expected null or string"
    if isinstance(default, bool):
        if isinstance(value, bool):
            return True, value, ""
        return False, value, "expected boolean"
    if isinstance(default, int):
        if isinstance(value, int) and not isinstance(value, bool):
            return True, value, ""
        return False, value, "expected integer"
    if isinstance(default, str):
        if isinstance(value, str):
            return True, value, ""
        return False, value, "expected string"
    if isinstance(default, list):
        if isinstance(value, list):
            return True, value, ""
        return False, value, "expected list"
    if isinstance(default, dict):
        if isinstance(value, dict):
            return True, value, ""
        return False, value, "expected object"

    if isinstance(value, type(default)):
        return True, value, ""
    return False, value, f"expected {type(default).__name__}"


def normalize_generation_mode(value) -> str:
    """Return a supported generation mode, preserving the API Portal-ready default."""
    text = str(value or "").strip()
    for mode in GENERATION_MODES:
        if text.lower() == mode.lower():
            return mode
    return DEFAULT_GENERATION_MODE


def normalize_x_info_options(value=None) -> dict:
    """Return supported x-info extension flags with defaults for missing values."""
    options = dict(DEFAULT_X_INFO_OPTIONS)
    if isinstance(value, dict):
        for name in options:
            if name in value:
                options[name] = bool(value[name])
    return options


def x_info_options_from_preferences(preferences: dict) -> dict:
    """Build generator x-info options from persisted preference keys."""
    return {
        name: bool(preferences.get(pref_key, True))
        for name, pref_key in X_INFO_EXTENSION_OPTION_KEYS.items()
    }


class PreferencesManager:
    """Manages user preferences with JSON persistence."""

    DEFAULT_PREFERENCES = {
        # Paths
        "remember_paths": True,  # Default: Remember last used paths
        "excel_input_folder": "",  # Specific preference (alias template_directory)
        "excel_output_folder": "", # Specific preference for Tab 1
        "oas_folder": "",  # Key for generated OAS
        
        # Persistence (Last Session State)
        "last_excel_input": "",
        "last_excel_output": "",
        "last_oas_folder": "",
        "last_designer_oas_import_folder": "",
        "last_legacy_src": "",
        "last_legacy_dst": "",
        "last_legacy_master": "",
        "last_api_model_workspace": "",
        "last_designer_oas_import_file": "",
        # Generation Options
        "gen_oas_30": True,
        "gen_oas_31": True,
        "gen_oas_swift": False,
        "generation_mode": DEFAULT_GENERATION_MODE,
        "gen_x_info_creation_date": True,
        "gen_x_info_release": True,
        "gen_x_info_customization": True,
        "gen_x_info_oasis_version": True,
        "excel_gen_attr_diff": True,
        "excel_gen_line_diff": False,
        # File Display
        "file_sort_order": "alphabetical",  # alphabetical, newest_first, oldest_first
        # View Options
        "yaml_theme": "oas-dark",
        "yaml_font": "Consolas",
        "yaml_font_size": 12,
        "yaml_word_wrap": False,
        # Log Appearance
        "gen_log_theme": "Light",
        "import_log_theme": "Light", # New: Excel to OAS Log
        "app_log_theme": "Dark",     # Added missing key
        "analysis_log_theme": "Light",
        "spectral_log_theme": "Dark",
        # Interface
        "default_tab": "OAS Generation",  # OAS Generation, Validation, View, Designer when enabled
        "enable_api_designer": False,
        "update_check_enabled": True,
        "update_manifest_url": DEFAULT_UPDATE_MANIFEST_URL,
        "update_download_url": "",
        "linter_engine": "spectral",  # spectral or vacuum
        "ignore_bad_request": True,
        "validation_font_size": 11,
        "remember_window_pos": False,
        "window_geometry": None,  # "WxH+X+Y" format
        # Documentation Viewer
        "doc_snap_default_enabled": False,  # Whether doc window snaps to main on open
        
        # Tools Settings
        "tools_legacy_tracing_enabled": True,
        "tools_legacy_example_tracing_enabled": True,
        "tools_legacy_collision_include_descriptions": False,
        "tools_legacy_collision_include_examples": False,
        "tools_legacy_capitalize_schema_names": True,
        "tools_legacy_fill_fix_examples": True,
        "tools_legacy_contact_name": "",
        "tools_legacy_contact_url": "",
        "tools_legacy_release": "",
        "tools_legacy_filename_pattern": "",
        "tools_legacy_swift_service": "",
        "swift_services": DEFAULT_SWIFT_SERVICES,
        "swift_servers_column_widths": {"service": 90, "url": 300, "description": 180},
        
        # OAS Diff Settings
        "diff_old_spec": "",
        "diff_new_spec": "",
        "diff_output_dir": "",
        "diff_static_variables": {
            "author": "",
            "company": "",
            "project_name": ""
        },
        "diff_template_synthesis": "",
        "diff_template_analytical": "",
        "diff_template_impact": "",
        "diff_template_compatibility": "",
        "diff_selected_reports": ["synthesis", "analytical", "impact", "compatibility"],
        "diff_show_enum_order_changes": False,
        "diff_show_validation_rule_only_description_changes": True,
        "diff_debug_mode": False,

        
        # Restored Functional Keys (mistakenly treated as orphans)
        "import_source_file": "",       # Tab 1: OAS Source File
        "search_history": [],           # Find functionality history
    }

    def __init__(self):
        self.preferences = deepcopy(self.DEFAULT_PREFERENCES)
        self._config_path = self._get_config_path()
        self.load()
        self.cleanup_orphans() # Auto-cleanup on load

    def _get_config_path(self) -> Path:
        """Get the path to the preferences file."""
        # Try to use AppData on Windows, home dir on others
        if os.name == "nt":
            app_data = os.environ.get("APPDATA", "")
            if app_data:
                config_dir = Path(app_data) / "OASIS"
            else:
                config_dir = Path.home() / ".oasis"
        else:
            config_dir = Path.home() / ".oasis"

        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "preferences.json"

    def get_config_dir(self) -> Path:
        """Return the user configuration directory used by OASIS."""
        return self._config_path.parent

    def get_legacy_example_seed_values_path(self) -> Path:
        """Return the editable seed-values file used by the legacy converter."""
        return self.get_config_dir() / "legacy_example_seed_values.yaml"

    def get_legacy_example_semantic_rules_path(self) -> Path:
        """Return the editable semantic-rules file used by the legacy converter."""
        return self.get_config_dir() / "legacy_example_semantic_rules.yaml"

    def load(self):
        """Load preferences from JSON file."""
        try:
            if self._config_path.exists():
                with open(self._config_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    
                    saved = migrate_saved_preferences(saved)
                    
                    # Merge with defaults (load all saved keys)
                    for key, value in saved.items():
                        self.preferences[key] = value
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load preferences: {e}")

    def cleanup_orphans(self):
        """Remove keys that are not in DEFAULT_PREFERENCES."""
        orphans = [k for k in self.preferences if k not in self.DEFAULT_PREFERENCES]
        if orphans:
            print(f"Removing orphan keys: {orphans}")
            for k in orphans:
                del self.preferences[k]
            self.save()

    def save(self):
        """Save preferences to JSON file."""
        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self.preferences, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save preferences: {e}")

    def get(self, key: str, default=None):
        """Get a preference value."""
        return self.preferences.get(key, default)

    def set(self, key: str, value):
        """Set a preference value."""
        self.preferences[key] = value

    def reset_to_defaults(self):
        """Reset all preferences to default values."""
        self.preferences = deepcopy(self.DEFAULT_PREFERENCES)
        self.save()

    def get_all(self) -> dict:
        """Get all preferences as a dictionary."""
        return deepcopy(self.preferences)

    def update(self, new_prefs: dict):
        """Update multiple preferences at once."""
        for key, value in new_prefs.items():
            self.preferences[key] = value

    def apply_overrides(self, overrides: dict) -> tuple[list[str], list[tuple[str, str]]]:
        """Apply validated manifest-driven preference overrides."""
        applied = []
        skipped = []
        if not isinstance(overrides, dict):
            return applied, [("<manifest>", "preferences_override must be an object")]

        for key, value in overrides.items():
            valid, normalized, reason = validate_preference_value(key, value)
            if not valid:
                skipped.append((str(key), reason))
                continue
            if self.preferences.get(key) != normalized:
                self.preferences[key] = normalized
                applied.append(key)

        if applied:
            self.save()
        return applied, skipped
