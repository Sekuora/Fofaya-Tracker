import os
import json

class SettingsData:
    def __init__(self):
        self.settings_file = './settings.json'
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w') as f:
                json.dump({
                    'minimized_to_tray': False,
                    'added_to_startup': False
                }, f)

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {
                'minimized_to_tray': False,
                'added_to_startup': False
            }
            self.save_settings()
        return self.settings

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)