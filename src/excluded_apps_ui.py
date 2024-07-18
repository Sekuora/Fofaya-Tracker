from PySide6.QtCore import Qt
from PySide6.QtGui import  QIcon
from PySide6.QtWidgets import (
                               QVBoxLayout, QWidget, QMessageBox, 
                                
                               QSizePolicy, QPushButton,
                               QTableWidgetItem, QTableWidget)

from .main_window_ui import MainWindow
from .time_track_data import TimeTrackData

class ExcludedAppsWindow(MainWindow):
    def __init__(self, time_tracker, settings_data=None):
        super().__init__(tracker=time_tracker, settings_data=settings_data)
        
        self.get_icons_path()

        self.set_initial_values()
        # Create MessageBox Style
        self.msg_style = """
            QMessageBox {
                background-color: rgba(35, 35, 35, 0.8);
                color: #ffffff;
                border: 2px solid rgba(70, 70, 70, 0.8);
                border-radius: 2px; /* Set border radius for the entire QMessageBox */
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #555;
                color: #ffffff;
            }
        """

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
                color: rgba(230, 230, 230, 0.8);
                background-color: rgba(30, 30, 30, 0.7);
                border: 0px solid rgba(70, 70, 70, 0.8);
                margin: 5px;
                border-radius: 0px;
            }
            QTableWidget::item {
                height: 30px;
                border-radius: 0px;
                border: 0px solid rgba(70, 70, 70, 0.8);
            }
            QTableWidget QHeaderView::section {
                color: white;
                background-color: rgba(70, 70, 70, 0.8);
                border-radius: 0px;
                border: 0px solid rgba(70, 70, 70, 0.8);
            }
            QTableWidget QPushButton {
                color: rgba(70, 70, 70, 0.8);
                background-color: rgba(50, 50, 50, 0.8);
                border: 0px solid rgba(70, 70, 70, 0.8);
                border-radius: 10px;
            }
            QTableWidget QPushButton:hover {
                color: rgba(210, 210, 210, 0.8);
                background-color: rgba(70, 70, 70, 0.8);
                border: 0px solid rgba(70, 70, 70, 0.8);
                border-radius: 0px;
            }
            QTableWidget::corner {
                background-color: rgba(40, 40, 40, 1.0); /* Set the background color of the corner handle */
                color: rgba(40, 40, 40, 1.0); /* Set the text color of the corner handle */
                border: 0px solid rgba(70, 70, 70, 0.8);
                border-radius: 0px; /* Set border radius to 0 */
            }
        """

        self.tracker_data = TimeTrackData() # Create an instance of TimeTrackData

        self.tracker = time_tracker
        
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


        # Load the time tracking data
        app_times = self.tracker_data.load_times()
        
        # Create a table
        self.table = QTableWidget()
        self.table.setStyleSheet(self.table_style)

        # Set the column count
        self.table.setColumnCount(2)  # Increase column count to 2

        # Set the header labels
        self.table.setHorizontalHeaderLabels(["Application", "Action"])  # Add "Action" header for the new column

        # For each application in the time tracking data
        for i, app in enumerate(app_times.keys()):
            # Add a new row to the table
            self.table.insertRow(i)
            
            # Add the application name to the table
            self.table.setItem(i, 0, QTableWidgetItem(app))

            # Create a "Delete" button
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet(self.button_style)
            delete_button.clicked.connect(lambda checked=False, app=app: self.delete_entry_button(app))
            self.table.setCellWidget(i, 1, delete_button)

            # Add the "Delete" button to the table
            self.table.setCellWidget(i, 1, delete_button)  # Add the button to the second column

        # Add the table to the layout
        self.layout.addWidget(self.table)

        # Create a widget and set the layout to it
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        # Set the widget as the central widget of the window
        self.setCentralWidget(self.widget)

        self.setWindowIcon(QIcon(self.window_icon_path))

    def delete_entry_button(self, app_name):
        # Create a confirmation dialog
        confirm_dialog = QMessageBox()
        confirm_dialog.setStyleSheet(self.msg_style)
        confirm_dialog.setIcon(QMessageBox.Warning)
        confirm_dialog.setText(f"Are you sure you want to delete all logs for '{app_name}'?")
        confirm_dialog.setWindowTitle("Confirm Deletion")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Make the dialog frameless
        confirm_dialog.setWindowFlags(Qt.FramelessWindowHint)

        # Show the dialog and get the user's response
        response = confirm_dialog.exec_()

        # If the user clicked "Yes", delete the entry
        if response == QMessageBox.Yes:
            # Delete the entry from the time tracking data
            self.tracker_data.delete_entry(app_name)

            # Find the row with the app_name and remove it
            for i in range(self.table.rowCount()):
                if self.table.item(i, 0).text() == app_name:
                    self.table.removeRow(i)
                    break

    def closeEvent(self, event):
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
        self.resize(460, 460)
        self.setMinimumSize(460, 460)
        self.setMaximumSize(460, 1080)
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

    def closeEvent(self, event):
        # Close the window after the animation has started
        self.close()

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