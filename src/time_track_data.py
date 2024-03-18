# time_track_data.py module
import os
import json
from .tracker_globals import process_time

class TimeTrackData:
    def __init__(self):
        self.filename = './app_times.json'  # Define the filename attribute
        self.excluded_apps_filename = './excluded_apps.json'  # Define the filename for excluded apps
        # Create the file if it doesn't exist
        # Create the files if they don't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

        if not os.path.exists(self.excluded_apps_filename):
            with open(self.excluded_apps_filename, 'w') as f:
                json.dump({"excluded_apps": {}}, f)  # Initialize as an empty dictionary, not a list


        

    def load_times(self):
        try:
            with open(self.filename, 'r') as f:
                existing_data = json.load(f)
                for app, dates in existing_data.items():
                    if app not in process_time:
                        process_time[app] = {}
                    for date, time in dates.items():
                        process_time[app][date] = time
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return process_time
    
    def save_times(self):
        try:
            with open(self.filename, 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        for app, dates in process_time.items():
            if app not in existing_data:
                existing_data[app] = {}
            for date, time in dates.items():
                existing_data[app][date] = time

        with open(self.filename, 'w') as f:
            json.dump(existing_data, f, indent=4)
            
        
    def load_excluded_apps(self):
        try:
            with open(self.excluded_apps_filename, 'r') as f:
                data = json.load(f)
                excluded_apps = data if isinstance(data, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError):
            excluded_apps = {"Fofaya": True}  # Initialize with "Fofaya Tracker" set to True

        # Load the app_times data
        try:
            with open(self.filename, 'r') as f:  # replaced self.app_times_filename with self.filename
                app_times = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            app_times = {}

        # Add any apps from the app_times data that aren't already in the excluded_apps dictionary
        for app in list(app_times):
            if app not in excluded_apps:
                excluded_apps[app] = False

        # Always include "Fofaya Tracker" in the dictionary of excluded apps
        excluded_apps["Fofaya Tracker"] = True

        # Save the updated excluded_apps dictionary
        with open(self.excluded_apps_filename, 'w') as f:
            json.dump(excluded_apps, f)

        return excluded_apps

    def save_excluded_apps(self, excluded_apps_dict):
        with open(self.excluded_apps_filename, 'w') as f:
            json.dump(excluded_apps_dict, f, indent=4)

    
    def update_excluded_app(self, app, state):
        # Load the current excluded apps
        excluded_apps = self.load_excluded_apps()

        # Update the state of the app
        excluded_apps[app] = state

        # Save the updated excluded apps
        self.save_excluded_apps(excluded_apps)