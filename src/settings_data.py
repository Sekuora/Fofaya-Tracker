import os
import json

class SettingsData:
    def __init__(self):
        self.settings_file = './settings.json'
        self.default_settings = {
            'minimized_to_tray': False,
            'added_to_startup': False,
            'instance_count': 0  # Add this field to manage instance count
        }
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = self.default_settings.copy()
            self.save_settings()
        return self.settings

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def increment_instance_count(self):
        if 'instance_count' not in self.settings:
            self.settings['instance_count'] = 0
        self.settings['instance_count'] += 1
        self.save_settings()
        return self.settings['instance_count'] == 1  # Return True if this is the first instance

    def decrement_instance_count(self):
        if 'instance_count' in self.settings and self.settings['instance_count'] > 0:
            self.settings['instance_count'] -= 1
            self.save_settings()
        return self.settings['instance_count']
