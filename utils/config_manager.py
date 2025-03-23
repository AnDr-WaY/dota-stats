import os
import json
import platform

class ConfigManager:
    """
    Manager for application configuration settings.
    Handles loading, saving, and updating configuration settings.
    """
    def __init__(self, app_name="DotaStats"):
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_config = {
            "theme": {
                "mode": "System",  # Light, Dark, System
                "color_scheme": "#0078D7",  # Blue default
                "opacity": 1.0
            }
        }
        
        # Create config directory if it doesn't exist
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        # Load or create config file
        self.config = self.load_config()
        
    def _get_config_directory(self):
        """Get the appropriate directory for storing configuration based on OS"""
        system = platform.system()
        
        if system == "Windows":
            return os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), self.app_name)
        elif system == "Darwin":
            return os.path.join(os.path.expanduser("~"), "Library", "Application Support", self.app_name)
        else:
            return os.path.join(os.path.expanduser("~"), ".config", self.app_name)
    
    def load_config(self):
        """Load configuration from file or create default if it doesn't exist"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Ensure all required keys exist by merging with default config
                return self._merge_configs(self.default_config, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config file: {e}")
                return self.default_config.copy()
        else:
            # Create new config file with default values
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def _merge_configs(self, default, user):
        """Recursively merge user config with default to ensure all keys exist"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
                
        return result
        
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
            
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except IOError as e:
            print(f"Error saving config file: {e}")
            return False
    
    def get_setting(self, section, key, default=None):
        """Get a specific setting value or default if not found"""
        try:
            if section in self.config and key in self.config[section]:
                return self.config[section][key]
        except Exception:
            pass
        return default
    
    def set_setting(self, section, key, value):
        """Set a specific setting value and save configuration"""
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
        self.save_config()
        
    def get_all_settings(self):
        """Get all configuration settings"""
        return self.config.copy() 