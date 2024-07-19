# app.py
# Copyright (C) 2024 Sekuora
# This file is part of a software tool distributed under the GNU General Public License.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Compile Instructions:
# 1. Ensure Python 3.x is installed on your system.
# 2. Optionally, create a virtual environment.
# 3. Install the required libraries by running `pip install -r requirements.txt`
# 4. PyInstaller is included in the requirements and it is what I used to compile the program.
# 5. Compile the program with `pyinstaller app.spec`.
# 6. The compiled program will be in the `dist` directory.
import os
import sys
import tempfile
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from src import TimeTrackData, MainWindow, TimeTracker, SettingsData

def get_icon_path():
    base_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(base_path)
    icon_path = os.path.join(parent_path, 'assets/fofaya_icon.ico')
    return icon_path

# Global variable to store the single instance of MainWindow
window = None

# Function to check if the application is already running
def is_already_running():
    lock_file = os.path.join(tempfile.gettempdir(), 'fofaya_app.lock')
    if os.path.exists(lock_file):
        return True
    with open(lock_file, 'w') as f:
        f.write(str(os.getpid()))
    return False

# Function to release the lock file when done
def release_lock():
    lock_file = os.path.join(tempfile.gettempdir(), 'fofaya_app.lock')
    if os.path.exists(lock_file):
        os.remove(lock_file)

def main():
    global window

    # Check if an instance of the application is already running
    if is_already_running():
        print("Another instance is already running.")
        sys.exit()  # Exit if another instance is running

    # Load tracker app data
    data = TimeTrackData()
    settings_data = SettingsData()
    settings_data.load_settings()
    data.load_times()

    # Create TimeTracker instance
    tracker = TimeTracker()

    # Create the application
    app = QApplication([])

    # Set the application icon
    app.setWindowIcon(QIcon(get_icon_path()))

    # Create a new MainWindow instance
    window = MainWindow(tracker, settings_data)

    if window.startup_minimized_tray:
        window.hide()
        window.trayIcon.show()
        window.start_tracking()
    else:
        window.show()
        window.trayIcon.show()

    # Connect the application exit signal to release the lock file
    app.aboutToQuit.connect(release_lock)

    app.exec()

    # Save the updated process_time
    data.save_times()

    # Save the updated settings
    settings_data.save_settings()

if __name__ == "__main__":
    main()
