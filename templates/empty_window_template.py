# log_window_ui.py
# Copyright (C) 2024 Sekuora
# This file is part of a software tool distributed under the GNU General Public License.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import json
import sys
from collections import defaultdict

from PySide6.QtCore import Qt, QTimer, QDate, QSize
from PySide6.QtGui import QColor, QTextCharFormat, QAction, QIcon
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, 
                               QPushButton, QVBoxLayout, QWidget, 
                               QCalendarWidget, QToolButton, QMenu, 
                               QWidgetAction, QSizePolicy)

from ..src.main_window_ui import MainWindow


class ExcludedAppsWindow(MainWindow):
    def __init__(self, time_tracker):
        super().__init__(tracker=time_tracker)
        # Create a layout and add the canvas to it
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2, 0, 2, 10)

        # Call top bar widget method
        top_bar_widget = self.top_bar()
        # Set the size policy of the top bar widget, so it doesn't expand
        top_bar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Set the alignment of the top bar widget to the top
        self.layout.addWidget(top_bar_widget, alignment=Qt.AlignTop)

        self.get_icons_path()

        self.set_initial_values()
     
        self.tracker = time_tracker


        top_bar_widget.setStyleSheet("background-color: rgba(40, 40, 40, 0.15); border: 0px solid rgba(70, 70, 70, 0.8); border-bottom: 0px solid rgba(70, 70, 70, 0.8);")  # 0.8 for 80% opacity

        # Create a widget and set the layout to it
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        # Set the widget as the central widget of the window
        self.setCentralWidget(self.widget)

        self.setWindowIcon(QIcon(self.window_icon_path))


    def widgets_initial_values(self):
        pass

    def widgets_small_screen_values(self):
        pass

    def widgets_minimum_size_values(self):
        pass

    def set_initial_values(self):
        # Set the window to be frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init_clock = True
        self.m_drag = False
        self.installEventFilter(self)
        self.normalGeometry = self.geometry()
        self.setWindowTitle("Fofaya Tracker")
        self.resize(720, 480)
        self.setMinimumSize(700, 460)
        self.setMaximumSize(1920, 1080)
        # Set the background color to a semi-transparent white
        self.setStyleSheet("""
                            background-color: rgba(30, 30, 30, 0.99); 
                            border-radius: 10px;
                            border: 2px solid rgba(50, 50, 50, 0.8);
                           margin-top: 0px;
                            """)
        
        
        self.m_mouse_down = False
        self.m_resize = False
        self.m_resize_direction = None
    
    def update_labels(self, app_name, timer):
        pass

    def idle_clock_startup(self):

        pass

    def contextMenuEvent(self, event):
        pass

    def toggleAlwaysOnTop(self, checked):
        pass