# time_tracker.py module
from PySide6.QtCore import QThread, Signal
import psutil
import win32process
import win32gui
from win32gui import GetForegroundWindow
import time
from .tracker_globals import process_time
from datetime import datetime
import pygetwindow as gw
from PySide6.QtCore import Signal
from .time_track_data import TimeTrackData  # Import TimeTrackData at the top of the file
import win32service


class TimeTracker(QThread):
    update_label = Signal(str, str)
    data_updated = Signal()  # New signal

    def __init__(self):
        super().__init__()
  
        self.is_running = False
        self.current_app = None
        self.time_track_data = TimeTrackData()  # Create an instance of TimeTrackData
        self.excluded_apps = {app: False for app in self.time_track_data.load_excluded_apps()}
      
        

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

    def get_current_app(self):
        try:
            # Get the foreground window
            hwnd = win32gui.GetForegroundWindow()

            # Get the process ID of the foreground window
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]

            # Check if the pid is a positive integer
            if pid > 0:
                # Get the process name using psutil
                process = psutil.Process(pid)
                process_name = process.name().replace(".exe", "")

                # Check if the process is a system process or located in the 'Windows' directory
                if process.username() in ['SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE'] or '\\Windows\\' in process.exe():
                    return "Idle"
                else:
                    # If the process name is already in the excluded_apps dictionary, return its value
                    if process_name in self.excluded_apps:
                        return self.excluded_apps[process_name]

                    # Get the text of the window's title bar
                    window_title = win32gui.GetWindowText(hwnd)

                    # If the window title is empty, use the process name
                    if not window_title:
                        window_title = process_name

                    # If the window title is not empty, format it
                    if window_title:
                        # Split the title by the dash and take the last part
                        app_name_split1 = window_title.split(" - ")[-1]
                        app_name_split2 = app_name_split1.split(": ")[-1].replace('\u200B', '')
                        # Check if the application name is too long or if it's in the excluded_apps list and its value is True
                        if len(app_name_split2) > 50 or (app_name_split2 in self.excluded_apps and self.excluded_apps[app_name_split2]) or app_name_split2 == "Fofaya":
                            return "Idle"
                        else:
                            # Add the app to the excluded_apps dictionary if it's not already there
                            if app_name_split2 not in self.excluded_apps:
                                self.excluded_apps[app_name_split2] = False
                            
                            window_title = app_name_split2

                    # Add the window title to the excluded_apps dictionary
                    self.excluded_apps[process_name] = window_title

                    # Return the app name
                    return window_title
            # If no window was found for the process, return "Idle"
            return "Idle"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return "Idle"
    def format_time(self, seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

  
        
        
    def format_time(self, seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def stop(self):
        self.is_running = False
    
    def is_running(self):
        return self.is_running