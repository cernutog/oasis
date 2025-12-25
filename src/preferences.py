"""
Preferences Manager for OAS Generation Tool.
Handles loading, saving, and providing default values for user preferences.
"""
import os
import json
from pathlib import Path


class PreferencesManager:
    """Manages user preferences with JSON persistence."""
    
    DEFAULT_PREFERENCES = {
        # Paths
        "template_directory": "",  # Empty = use relative default
        "oas_folder": "",  # Empty = use relative default
        
        # Generation Options
        "gen_oas_30": True,
        "gen_oas_31": True,
        "gen_oas_swift": False,
        
        # File Display
        "file_sort_order": "alphabetical",  # alphabetical, newest_first, oldest_first
        
        # View Options
        "yaml_theme": "oas-dark",
        "yaml_font": "Consolas",
        "yaml_font_size": 12,
        
        # Log Appearance
        "gen_log_theme": "Light",
        "analysis_log_theme": "Light",
        "spectral_log_theme": "Light",
        
        # Interface
        "default_tab": "Generation",  # Generation, Validation, View
        "ignore_bad_request": True,
        "remember_window_pos": True,
        "window_geometry": None,  # "WxH+X+Y" format
        
        # Documentation Viewer
        "doc_snap_default_enabled": False,  # Whether doc window snaps to main on open
    }
    
    def __init__(self):
        self.preferences = dict(self.DEFAULT_PREFERENCES)
        self._config_path = self._get_config_path()
        self.load()
    
    def _get_config_path(self) -> Path:
        """Get the path to the preferences file."""
        # Try to use AppData on Windows, home dir on others
        if os.name == 'nt':
            app_data = os.environ.get('APPDATA', '')
            if app_data:
                config_dir = Path(app_data) / 'OAS_Generation_Tool'
            else:
                config_dir = Path.home() / '.oas_generation_tool'
        else:
            config_dir = Path.home() / '.oas_generation_tool'
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'preferences.json'
    
    def load(self):
        """Load preferences from JSON file."""
        try:
            if self._config_path.exists():
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    # Merge with defaults (load all saved keys)
                    for key, value in saved.items():
                        self.preferences[key] = value
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load preferences: {e}")
    
    def save(self):
        """Save preferences to JSON file."""
        try:
            with open(self._config_path, 'w', encoding='utf-8') as f:
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
        self.preferences = dict(self.DEFAULT_PREFERENCES)
    
    def get_all(self) -> dict:
        """Get all preferences as a dictionary."""
        return dict(self.preferences)
    
    def update(self, new_prefs: dict):
        """Update multiple preferences at once."""
        for key, value in new_prefs.items():
            self.preferences[key] = value
