# time_tracker.py module
# Copyright (C) 2024 Sekuora
# This file is part of a software tool distributed under the GNU General Public License.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from PySide6.QtCore import QThread, Signal
import psutil
import win32process
import win32gui
import time
from .tracker_globals import process_time
from datetime import datetime
from .time_track_data import TimeTrackData  # Import TimeTrackData at the top of the file
import win32api


class TimeTracker(QThread):
    update_label = Signal(str, str)
    data_updated = Signal()  # New signal
    def __init__(self):
        super().__init__()
  
        self.is_running = False
        self.current_app = None
        self.time_track_data = TimeTrackData()  # Create an instance of TimeTrackData
        self.excluded_apps = ["Fofaya"]

    # In TimeTracker class
    def run(self):

        global process_time
        self.is_running = True
        save_counter = 0
        while self.is_running:
            start_time = time.time()

            new_app = self.get_current_app()
            if new_app is not None and new_app != self.current_app:  # Check if the current app is in the ignore list
                self.current_app = new_app
                current_date = datetime.now().strftime('%d/%m/%Y')
                if self.current_app not in process_time.keys():
                    process_time[self.current_app] = {}
                if current_date not in process_time[self.current_app].keys():
                    process_time[self.current_app][current_date] = 0

            if self.current_app is not None and self.current_app != "Idle":
                current_date = datetime.now().strftime('%d/%m/%Y')
                process_time[self.current_app][current_date] += 1
                formatted_time = self.format_time(process_time[self.current_app][current_date])
            else:
                formatted_time = "00:00:00"

            self.update_label.emit(self.current_app, formatted_time)

            save_counter += 1
            if save_counter >= 10:
                self.time_track_data.save_times()
                self.data_updated.emit()  # Emit signal when data is updated
                save_counter = 0  # Reset the counter

            end_time = time.time()
            execution_time = end_time - start_time
            sleep_time = max(1.0 - execution_time, 0)
            time.sleep(sleep_time)
    
    def get_window_title(self, pid):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return win32gui.GetWindowText(hwnds[0]) if hwnds else None
    
    def is_helpful(self, name):
        return name and len(name) <= 50

    def get_current_app(self):
        try:
            # Get the foreground window
            hwnd = win32gui.GetForegroundWindow()

            # Get the process ID of the foreground window
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]

            # Check if the pid is a positive integer
            if pid > 0:
                # Get the process using psutil
                process = psutil.Process(pid)
                
                # Get the executable path
                exe_path = process.exe()
                
                # Check if the process is a system process or located in the 'Windows' directory
                if process.username() in ['SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE'] or '\\Windows\\' in exe_path:
                    return "Idle"

                # Get product name and file description from the executable metadata
                product_name = self.get_product_name(exe_path)
                file_description = self.get_file_description(exe_path)
                
                # Get the exe name and format it nicely
                exe_name = process.name().replace(".exe", "").replace("_", " ").title()

                # Create a dictionary to map specific exe names to their desired display names
                exe_name_mapping = {
                    "Epicgameslauncher": "Epic Games Launcher"
                    # Add more mappings here if needed
                }

                # If exe name is in the mapping, use the mapped name
                if exe_name in exe_name_mapping:
                    app_name = exe_name_mapping[exe_name]
                elif product_name and self.is_helpful(product_name):
                    app_name = product_name
                elif file_description and self.is_helpful(file_description):
                    app_name = file_description
                else:
                    app_name = exe_name
                
                # Check if the app is in the exclusions list
                if app_name in self.excluded_apps:
                    return "Idle"

                  # Check if the app is in the excluded_apps dictionary
                # Check if the app is in the excluded_apps dictionary and if it's set to True
                # Return the app name
                return app_name
            # If no window was found for the process, return "Idle"
            return "Idle"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return "Idle"
    
    def get_file_description(self, exe_path):
        try:
            # Get file description from executable metadata
            file_description = win32api.GetFileVersionInfo(exe_path, '\\StringFileInfo\\040904b0\\FileDescription')
            return file_description
        except Exception as e:
            print(f"Error retrieving file description: {e}")
            return None

    def get_product_name(self, exe_path):
        try:
            # Get product name from executable metadata
            product_name = win32api.GetFileVersionInfo(exe_path, '\\StringFileInfo\\040904b0\\ProductName')
            return product_name
        except Exception as e:
            print(f"Error retrieving product name: {e}")
            return None

    def format_time(self, seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))
    
    def format_time(self, seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def stop(self):
        self.is_running = False
    
    def is_running(self):
        return self.is_running