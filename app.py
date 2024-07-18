# app.py
# Copyright (C) 2024 Sekuora
# This file is part of a software tool distributed under the GNU General Public License.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Compile Instructions:
# 1. Ensure Python 3.x is installed on your system.
# 2. Optionally, create a virtual environment.
# 3. Install the required libraries by running pip install -r requirements.txt
# 4. PyInstaller is included in the requirements and it is what I used to compile the program.
# 5. Compile the program with pyinstaller app.spec.
# 6. The compiled program will be in the dist directory.

import os
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory, QSystemSemaphore, QByteArray, QDataStream, QIODevice
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from src import TimeTrackData, MainWindow, TimeTracker, SettingsData

def get_icon_path():
    base_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(base_path)
    icon_path = os.path.join(parent_path, 'assets/fofaya_icon.ico')
    return icon_path

def send_message_to_existing_instance():
    socket = QLocalSocket()
    socket.connectToServer("FofayaTrackerServer")
    if socket.waitForConnected(1000):
        socket.write(b"SHOW")
        socket.flush()
        socket.waitForBytesWritten(1000)
        socket.close()

def main():
    # Ensure a single instance using QSharedMemory
    shared_memory = QSharedMemory("FofayaTrackerSharedMemory")
    if not shared_memory.create(1):
        send_message_to_existing_instance()
        sys.exit(0)

    # Create the application
    app = QApplication([])

    # Set the application icon
    app.setWindowIcon(QIcon(get_icon_path()))

    # Load tracker app data
    data = TimeTrackData() 
    settings_data = SettingsData()
    settings_data.load_settings()
    data.load_times()

    # Create TimeTracker instance
    tracker = TimeTracker()

    # Create the main window
    window = MainWindow(tracker, settings_data)

    # IPC server to handle messages from other instances
    server = QLocalServer()
    def handle_new_connection():
        socket = server.nextPendingConnection()
        if socket.waitForReadyRead(1000):
            message = socket.readAll().data().decode()
            if message == "SHOW":
                if window.isMinimized() or not window.isVisible():
                    window.show()
                    window.raise_()
                    window.activateWindow()
                    window.trayIcon.hide()

    server.newConnection.connect(handle_new_connection)
    if not server.listen("FofayaTrackerServer"):
        if server.serverError() == QLocalServer.AddressInUseError:
            QLocalServer.removeServer("FofayaTrackerServer")
            server.listen("FofayaTrackerServer")

    if window.startup_minimized_tray:
        window.hide()
        window.trayIcon.show()
        window.startTrackingAction()
    else:
        window.show()
        window.trayIcon.show()

    app.exec()

    # Save the updated process_time
    data.save_times()

    # Save the updated settings
    settings_data.save_settings()

if __name__ == "__main__":
    main()
