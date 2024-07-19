import os
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox
from src import TimeTrackData, MainWindow, TimeTracker, SettingsData
import atexit

def get_icon_path():
    base_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(base_path)
    icon_path = os.path.join(parent_path, 'assets/fofaya_icon.ico')
    return icon_path

# Function to clean up stale instance count
def reset_stale_instance_count():
    settings_data.load_settings()
    if settings_data.settings['instance_count'] > 0:
        # Attempt to verify if the application is running
        # If not running, reset instance count
        # You might need an additional check here, for example a PID file or other method.
        # For now, we'll assume the instance count should be reset.
        settings_data.settings['instance_count'] = 0
        settings_data.save_settings()

# Load tracker app data
data = TimeTrackData()
settings_data = SettingsData()
settings_data.load_settings()
data.load_times()

# Create TimeTracker instance
tracker = TimeTracker()

# Check if another instance is running
reset_stale_instance_count()  # Ensure stale counts are reset
if not settings_data.increment_instance_count():
    # Show message and exit if another instance is running
    app = QApplication(sys.argv)
    QMessageBox.warning(None, 'Fofaya Tracker', 'Another instance is already running.')
    sys.exit()

# Create the application
app = QApplication([])

# Set the application icon
app.setWindowIcon(QIcon(get_icon_path()))

# Create the main window
window = MainWindow(tracker, settings_data)

if window.startup_minimized_tray:
    window.hide()
    window.trayIcon.show()
    window.tracking_onDemand()
else:
    window.show()
    window.trayIcon.show()

# Define cleanup function to decrement the counter on exit
def cleanup():
    settings_data.decrement_instance_count()

# Connect the cleanup function to the app's aboutToQuit signal
app.aboutToQuit.connect(cleanup)

# Ensure cleanup happens if the application exits unexpectedly
atexit.register(cleanup)

app.exec()

# Save the updated process_time
data.save_times()

# Save the updated settings
settings_data.save_settings()
