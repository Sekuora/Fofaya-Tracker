# time_track_data.py module
# Copyright (C) 2024 Sekuora
# This file is part of a software tool distributed under the GNU General Public License.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import os
import json
from .tracker_globals import process_time

class TimeTrackData:
    def __init__(self):
        self.filename = './app_times.json'  # Define the filename attribute
       
        # Create the files if they don't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

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
    
    def delete_entry(self, app_name):
        try:
            # Load the existing data from the file
            with open(self.filename, 'r') as f:
                existing_data = json.load(f)

            # Delete the entry if it exists
            if app_name in existing_data:
                del existing_data[app_name]
                # Also delete the entry from the process_time global variable
                if app_name in process_time:
                    del process_time[app_name]
            else:
                print(f"App name '{app_name}' not found in the existing data.")

            # Write the updated data back to the file
            with open(self.filename, 'w') as f:
                json.dump(existing_data, f)
        except IOError as e:
            print(f"An error occurred while accessing the file: {e}")
        except json.JSONDecodeError as e:
            print(f"An error occurred while decoding the JSON data: {e}")