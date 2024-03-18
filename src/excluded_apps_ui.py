import json
import sys
import os
import win32api
from collections import defaultdict

from PySide6.QtCore import Qt, QTimer, QDate, QSize
from PySide6.QtGui import QColor, QTextCharFormat, QAction, QIcon
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, 
                               QPushButton, QVBoxLayout, QWidget, 
                               QCalendarWidget, QToolButton, QMenu, 
                               QWidgetAction, QSizePolicy, QFileDialog, QCheckBox,
                               QListWidget, QListWidgetItem, QTableWidgetItem, QTableWidget)

from .main_window_ui import MainWindow
from .time_track_data import TimeTrackData

import ctypes

class ExcludedAppsWindow(MainWindow):
    def __init__(self, time_tracker):
        super().__init__(tracker=time_tracker)
                # Create the qpushbutton style
        self.button_style = """
                QPushButton {
                    background-color: rgba(43, 43, 43, 0.7);
                    border-radius: 50px;
                    color: rgba(210, 210, 210, 0.8);
                    border: 0px solid rgba(70, 70, 70, 0.8);
                    margin-bottom: 2px;
                }
                QPushButton:pressed {
                    background-color: rgba(47, 47, 47, 0.7);
                    color: rgba(222, 222, 222, 1);                       
                }
                QPushButton:hover {
                    background-color: rgba(45, 45, 45, 0.7);
                    color: rgba(230, 230, 230, 0.9);
                }
                QPushButton:checked {
                    background-color: rgba(44, 44, 44, 0.7);
                    color: rgba(232, 232, 232, 0.8);
                }
                QPushButton:checked:pressed {
                    background-color: rgba(51, 51, 51, 0.7);
                    color: rgba(232, 232, 232, 1);
                }
                QPushButton:checked:hover {
                    background-color: rgba(45, 45, 45, 0.7);
                    color: rgba(230, 230, 230, 0.9);
                }
        """

        self.table_style = """
            QTableWidget {
                color: rgba(210, 210, 210, 0.8);
                background-color: rgba(43, 43, 43, 0.7);
                border: 0px solid rgba(70, 70, 70, 0.8);
                margin: 5px;
                border-radius: 0px;
            }
            QTableWidget::item {
                height: 30px;
                border-radius: 0px;
            }
            QTableWidget QHeaderView::section {
                color: rgba(43, 43, 43, 0.7);
                background-color: rgba(210, 210, 210, 0.8);
                border-radius: 0px;
            }
            QTableWidget QPushButton {
                color: rgba(70, 70, 70, 0.8);
                border-radius: 0px;
            }
            QTableWidget QPushButton:hover {
                color: rgba(210, 210, 210, 0.8);
                border-radius: 0px;
            }
        """



        self.tracker_data = TimeTrackData() # Create an instance of TimeTrackData
        



        # Create a layout and add the canvas to it
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2, 0, 2, 10)

        # Call top bar widget method
        top_bar_widget = self.top_bar()
        top_bar_widget.setStyleSheet("background-color: rgba(40, 40, 40, 0.15); border: 0px solid rgba(70, 70, 70, 0.8); border-bottom: 0px solid rgba(70, 70, 70, 0.8);")  # 0.8 for 80% opacity

        # Set the size policy of the top bar widget, so it doesn't expand
        top_bar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Set the alignment of the top bar widget to the top
        self.layout.addWidget(top_bar_widget, alignment=Qt.AlignTop)

        self.get_icons_path()

        self.set_initial_values()
     
        self.tracker = time_tracker
        

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["App", "Track"])
        self.table_widget.setStyleSheet(self.table_style)
        self.layout.addWidget(self.table_widget)

        # Load the excluded apps data
        self.load_excluded_apps()


        # Create a widget and set the layout to it
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        # Set the widget as the central widget of the window
        self.setCentralWidget(self.widget)

        self.setWindowIcon(QIcon(self.window_icon_path))




    def load_excluded_apps(self):
        excluded_apps = self.tracker_data.load_excluded_apps()
        self.table_widget.setRowCount(len(excluded_apps))
        for i, (app, track) in enumerate(excluded_apps.items()):
            self.table_widget.setItem(i, 0, QTableWidgetItem(app))
            checkbox = QCheckBox()
            checkbox.setChecked(not track)
            checkbox.stateChanged.connect(lambda state, app=app: self.update_excluded_app(app, state))
            layout = QHBoxLayout()
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            widget = QWidget()
            widget.setLayout(layout)
            self.table_widget.setCellWidget(i, 1, widget)

    def update_excluded_app(self, app, state):
        self.tracker_data.update_excluded_app(app, state == 2)
    
    def update_excluded_apps(self):
        excluded_apps = self.tracker_data.load_excluded_apps()
        
        for i in range(self.table_widget.rowCount()):
            app = self.table_widget.item(i, 0).text()
            checkbox = self.table_widget.cellWidget(i, 1).children()[1]
            excluded_apps[app] = checkbox.isChecked()

        self.tracker_data.save_excluded_apps(excluded_apps)

    def closeEvent(self, event):
        self.update_excluded_apps()
        super().closeEvent(event)


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

    def widgets_initial_values(self):
        pass

    def widgets_small_screen_values(self):
        pass

    def widgets_minimum_size_values(self):
        pass

    def update_labels(self, app_name, timer):
        pass

    def idle_clock_startup(self):

        pass

    def contextMenuEvent(self, event):
        pass

    def toggleAlwaysOnTop(self, checked):
        pass