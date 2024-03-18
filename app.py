import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from src import TimeTrackData, MainWindow, TimeTracker, process_time, recent_apps

def get_icon_path():
    # Get the path to the directory that contains the current file
    base_path = os.path.dirname(__file__)

    # Get the path to the parent directory
    parent_path = os.path.dirname(base_path)

    # Get the path to the icon file
    icon_path = os.path.join(parent_path, 'assets/fofaya_icon.ico')

    return icon_path

# Load tracker app data
data = TimeTrackData()
data.load_times()  # Update the global process_time variable directly

# Create TimeTracker instance
tracker = TimeTracker()

# Create the application
app = QApplication([])

# Set the application icon
app.setWindowIcon(QIcon(get_icon_path()))

# Create the main window
window = MainWindow(tracker)

window.show()

app.exec()

# Save the updated process_time
data.save_times()