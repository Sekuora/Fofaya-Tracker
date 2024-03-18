# excluded_apps.py module
import os
import json

class ExcludedApps:
    def __init__(self):
        self.filename = './excluded_apps.json'  # Define the filename attribute

        # Create the file if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

        self.load_apps()

    def load_apps(self):
        try:
            with open(self.filename, 'r') as f:
                self.excluded_apps = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.excluded_apps = {}

    def save_apps(self):
        with open(self.filename, 'w') as f:
            json.dump(self.excluded_apps, f, indent=4)

    def add_app(self, app, path):
        if app not in self.excluded_apps:
            self.excluded_apps[app] = path
            self.save_apps()

    def remove_app(self, app):
        if app in self.excluded_apps:
            del self.excluded_apps[app]
            self.save_apps()

    def is_excluded(self, app):
        return app in self.excluded_apps