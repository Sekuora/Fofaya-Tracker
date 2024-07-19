# main_window_ui.py
# Copyright (C) 2024 Sekuora
# This file is part of a software tool distributed under the GNU General Public License.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from PySide6.QtWidgets import QMainWindow, QLabel, QWidgetAction, QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QPalette, QColor, QFont, QIcon, QAction, QFontDatabase
from PySide6.QtCore import Qt, QSize, QPoint, QEvent, QTimer, QPropertyAnimation, QEasingCurve, QRect
import json
import sys
import getpass
import os
import win32com.client

class MainWindow(QMainWindow):
    def __init__(self, tracker, settings_data):

        super().__init__()
                # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Build the paths to the font files
        poppins_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'Poppins-Regular.ttf')
        azeret_mono_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'AzeretMono-Medium.ttf')
        # Build the path to the 'Poppins-SemiBold' font file
        poppins_semi_bold_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'Poppins-SemiBold.ttf')
        # Load 'Poppins SemiBold' font
        font_id = QFontDatabase.addApplicationFont(poppins_semi_bold_font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if len(font_families) > 0:
                self.poppins_semi_bold_font = font_families[0]
        else:
            print('Failed to load font.')

        # Load 'Poppins Regular' font
        font_id = QFontDatabase.addApplicationFont(poppins_font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if len(font_families) > 0:
                self.poppins_font = font_families[0]
        else:
            print('Failed to load font.')

        # Load 'Azeret Mono Medium' font
        font_id = QFontDatabase.addApplicationFont(azeret_mono_font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if len(font_families) > 0:
                self.azeret_mono_font = font_families[0]
        else:
            print('Failed to load font.')        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Build the paths to the font files
        poppins_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'Poppins-Regular.ttf')
        azeret_mono_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'AzeretMono-Medium.ttf')
        # Build the path to the 'Poppins-SemiBold' font file
        poppins_semi_bold_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'Poppins-SemiBold.ttf')
        # Load 'Poppins SemiBold' font
        font_id = QFontDatabase.addApplicationFont(poppins_semi_bold_font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if len(font_families) > 0:
                self.poppins_semi_bold_font = font_families[0]
        else:
            print('Failed to load font.')

        # Load 'Poppins Regular' font
        font_id = QFontDatabase.addApplicationFont(poppins_font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if len(font_families) > 0:
                self.poppins_font = font_families[0]
        else:
            print('Failed to load font.')

        # Load 'Azeret Mono Medium' font
        font_id = QFontDatabase.addApplicationFont(azeret_mono_font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if len(font_families) > 0:
                self.azeret_mono_font = font_families[0]
        else:
            print('Failed to load font.')


        # Loads the initial settings
        self.settings_data = settings_data
        self.added_to_startup = self.settings_data.settings.get('added_to_startup', False)
        self.minimized_to_tray = self.settings_data.settings.get('minimized_to_tray', False)
        self.startup_minimized_tray = self.settings_data.settings.get('startup_minimized_tray', False)

        # Get the paths to the icon files
        self.get_icons_path()

        # Get the paths to the icon files
        self.get_icons_path()
        
        # Create the top bar widget
        top_bar_widget = self.top_bar()

        self.Toolbutton_style = """
                QToolButton {
                    background-color: rgba(43, 43, 43, 0.7);
                    border-radius: 50px;
                    color: rgba(210, 210, 210, 0.8);
                    border: 0px solid rgba(70, 70, 70, 0.8);
                    margin-bottom: 2px;
                    padding-right: 10px;
                }
                QToolButton:pressed {
                    background-color: rgba(47, 47, 47, 0.7);
                    color: rgba(222, 222, 222, 1);                       
                }
                QToolButton:hover {
                    background-color: rgba(45, 45, 45, 0.7);
                    color: rgba(230, 230, 230, 0.9);
                }
                QToolButton:checked {
                    background-color: rgba(44, 44, 44, 0.7);
                    color: rgba(232, 232, 232, 0.8);
                }
                QToolButton:checked:pressed {
                    background-color: rgba(51, 51, 51, 0.7);
                    color: rgba(232, 232, 232, 1);
                }
                QToolButton:checked:hover {
                    background-color: rgba(45, 45, 45, 0.7);
                    color: rgba(230, 230, 230, 0.9);
                }
                
        """
   
        # Create a context menu
        tray_contextMenu = QMenu()
        tray_contextMenu.setTitle("Fofaya")

        # Create a start tracking action
        self.tray_start_tracking = False
        self.startTrackingAction = QAction("Start Tracking", self)
        self.startTrackingAction.setCheckable(True)  # Make the action checkable
        self.startTrackingAction.triggered.connect(self.toggle_tracking)  # Toggle tracking when this action is triggered
        tray_contextMenu.addAction(self.startTrackingAction)

        # Create a restore action
        restoreAction = QAction("Open Fofaya", self)
        restoreAction.triggered.connect(self.show)  # Show the main window when this action is triggered
        tray_contextMenu.addAction(restoreAction)

        # Create a quit action
        quitAction = QAction("Exit", self)
        quitAction.triggered.connect(QApplication.instance().quit)  # Close the application when this action is triggered
        tray_contextMenu.addAction(quitAction)

      

        # Create the system tray icon
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setToolTip("Fofaya Tracker")

        # Connect the activated signal to a method that handles the double-click event
        self.trayIcon.activated.connect(self.on_tray_icon_activated)
    

        # Set the context menu for the tray icon
        self.trayIcon.setContextMenu(tray_contextMenu)

        self.trayIcon.setIcon(QIcon(self.tray_icon_path))
   

        self.set_initial_values()
        self.setWindowIcon(QIcon(self.window_icon_path))
        

        # Create the animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(75)  # The animation lasts 500 ms

        # Set the easing curve
        self.animation.setEasingCurve(QEasingCurve.OutCubic)


        
        # Set the background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(50, 130, 180))
        self.setPalette(palette)

        # Define the widgets
        self.app_name_label = QLabel()
     
        self.timer_label = QLabel()

        self.start_button = QToolButton()
    

        self.widgets_initial_values()

        self.start_button.setVisible(True)
        self.start_button.setText('Start Tracking')

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.start_button)
        button_layout.addStretch(1)

        # Variables to store the mouse position
        self.m_mouse_down = False
        self.m_old_pos = None


        layout = QVBoxLayout()
        layout.setContentsMargins(2, 0, 2, 10)  # Remove the margins
  
        # Add the top bar layout to the main layout
        layout.addWidget(top_bar_widget)

    
        # Add widgets with stretch factors
        layout.addWidget(self.app_name_label, 1)
   
        layout.addWidget(self.timer_label, 1)
        layout.addLayout(button_layout, 2)

        # Add a stretch at the bottom
        layout.addStretch(1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.time_tracker = tracker
        self.time_tracker.update_label.connect(self.update_labels)


        
        # Call Idle state
        self.idle_clock_startup()

        self.updateUI()

        # Check Reset
        self.time_tracker.day_reset.connect(self.reset_tracking)
        

    def top_bar(self):
        # Top Bar
        # Create a QHBoxLayout for the top bar
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setSpacing(0) # Set the spacing between the widgets to 5 pixels

        # Add stretch to push the buttons to the right
        top_bar_layout.addStretch(1)

        # Create a QWidget for the top bar
        top_bar_widget = QWidget()

        # Set the layout of the widget to the top bar layout
        top_bar_widget.setLayout(top_bar_layout)
        top_bar_widget.setFixedHeight(25)  # Set the height of the widget to 50 pixels

        # Set the background color of the widget to white-ish using a style sheet
        top_bar_widget.setStyleSheet("background-color: rgba(40, 40, 40, 0.15); border: 0px solid rgba(70, 70, 70, 0.8);")  # 0.8 for 80% opacity

        # Create QToolButtons for the close, maximize, and minimize actions
        close_button = QToolButton()

 
        close_button.clicked.connect(self.close_window)
        close_button.setFixedHeight(20)  # Set the height to 30 pixels
        close_button.setFixedWidth(30)  # Set the width to 30 pixels
        close_button.setIconSize(QSize(20, 20))
        close_button.setIcon(QIcon(self.close_icon_path))
        close_button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border-right: 0px solid rgba(70, 70, 70, 0.8);
                border-left: 0px solid rgba(70, 70, 70, 0.8);
                border-radius: 0px;
                border-top-right-radius: 5px;
            }
            QToolButton:hover {
                background-color: rgba(255, 100, 100, 0.5);
            }
            """)
        

        maximize_button = QToolButton()
  
        maximize_button.clicked.connect(self.toggleMaximize)
        maximize_button.setFixedHeight(20)  # Set the height to 30 pixels
        maximize_button.setFixedWidth(30)  # Set the width to 30 pixels
        maximize_button.setIconSize(QSize(20, 20))
        maximize_button.setIcon(QIcon(self.maximize_icon_path))
        maximize_button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border-left: 0px solid rgba(70, 70, 70, 0.8);
                border-right: 0px solid rgba(70, 70, 70, 0.8);
                border-radius: 0px;
            }
            QToolButton:hover {
                background-color: rgba(200, 200, 200, 0.2);
            }
            """)

        minimize_button = QToolButton()
       
        minimize_button.clicked.connect(self.minimize)
        minimize_button.setFixedHeight(20)  # Set the height to 30 pixels
        minimize_button.setFixedWidth(30)  # Set the width to 30 pixels
        minimize_button.setIconSize(QSize(20, 20))
        minimize_button.setIcon(QIcon(self.minimize_icon_path))
        minimize_button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border-left: 0px solid rgba(70, 70, 70, 0.8);
                border-right: 0px solid rgba(70, 70, 70, 0.8);
                border-radius: 0px;
            }
            QToolButton:hover {
                background-color: rgba(200, 200, 200, 0.2);
            }
            """)
        

        # Add the buttons to the top bar layout
        top_bar_layout.addWidget(minimize_button)
        top_bar_layout.addWidget(maximize_button)
        top_bar_layout.addWidget(close_button)

        # Alignment with the buttons
        top_bar_layout.setAlignment(close_button, Qt.AlignVCenter)
        top_bar_layout.setAlignment(maximize_button, Qt.AlignVCenter)
        top_bar_layout.setAlignment(minimize_button, Qt.AlignVCenter)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        return top_bar_widget
    
    def get_icons_path(self):
        # Get the path to the directory that contains the current file
        base_path = os.path.dirname(__file__)

        # Get the path to the parent directory
        parent_path = os.path.dirname(base_path)

        # Get the paths to the icon files
        self.close_icon_path = os.path.join(parent_path, 'assets/x_button.png')
        self.maximize_icon_path = os.path.join(parent_path, 'assets/maximize.png')
        self.minimize_icon_path = os.path.join(parent_path, 'assets/minimize.png')
        self.window_icon_path = os.path.join(parent_path, 'assets/fofaya_icon.ico')
        self.tray_icon_path = os.path.join(parent_path, 'assets/fofaya_icon.ico')


    def create_shortcut(self, path, target='', wDir='', icon=''):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        if icon:
            shortcut.IconLocation = icon
        shortcut.save()

    def add_to_startup(self):
        self.get_icons_path()  # Call this to set window_icon_path
        username = getpass.getuser()
        startup_folder = os.path.join(os.path.expanduser('~'), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        target = sys.executable  # Use the location where your installer places the executable
        path = os.path.join(startup_folder, "Fofaya.lnk")
        wDir = os.path.dirname(target)
        icon = self.window_icon_path  # Use window_icon_path as the icon
        self.create_shortcut(path, target, wDir, icon)
        print(f"Shortcut created at {path}")

    def remove_from_startup(self):
        username = getpass.getuser()
        startup_folder = os.path.join(os.path.expanduser('~'), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        path = os.path.join(startup_folder, "Fofaya.lnk")
        if os.path.exists(path):
            os.remove(path)
        print(f"Shortcut removed from {path}")
        
    def set_icons(self):
        pass

    def idle_clock_startup(self):
        
        if self.init_clock:
            self.timer_label.setText("00:00:00")
            self.time_tracker.stop()
            self.app_name_label.setText("Idle")
        else:
            self.start_tracking()

    def set_initial_values(self):
        # Set the window to be frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init_clock = True
        self.m_drag = False
        self.installEventFilter(self)
        self.normalGeometry = self.geometry()
        self.setWindowTitle("Fofaya")
        self.resize(450, 320)
        self.setMinimumSize(150, 125)
        self.setMaximumSize(1920, 1080)
        # Set the background color to a semi-transparent white
        self.setStyleSheet("""
                            background-color: rgba(30, 30, 30, 1); 
                            border-radius: 10px;
                            border: 3px solid rgba(120, 120, 120, 1);
                            
                            """)
        
        self.m_mouse_down = False
        self.m_resize = False
        self.m_resize_direction = None

    def widgets_initial_values(self):
        if hasattr(self, 'app_name_label'):
            self.app_name_label.setFont(QFont(self.poppins_font, 19))
            self.app_name_label.setMinimumSize(QSize(100, 200))
            self.app_name_label.setAlignment(Qt.AlignCenter)
            self.app_name_label.setStyleSheet("""
                                            color: rgba(180, 180, 180, 1);
                                            margin-top: 125px; padding: 15px;
                                            margin-bottom: 0px;
                                            margin-right: 2px;
                                            margin-left: 2px;
                                            border: 0px solid rgba(90, 90, 90, 1);
                                            """)

        # Timer init values
        self.timer_label.setFont(QFont(self.azeret_mono_font, 95))
        self.timer_label.setMinimumSize(QSize(100, 200))
        self.timer_label.setStyleSheet("margin-bottom: 40px; color: rgba(210, 210, 210, 1); background-color: rgba(0, 0, 0, 0); border: solid 0px;")
        self.timer_label.setAlignment(Qt.AlignCenter)

        # Start Tracking Button init values
        self.start_button.clicked.connect(self.start_tracking)
        self.start_button.setFont(QFont(self.poppins_semi_bold_font, 24))
        self.start_button.setFixedWidth(300)
        self.start_button.setFixedHeight(105)
        self.start_button.setCheckable(True)
        self.start_button.setStyleSheet("""
            QToolButton {
                background-color: rgba(40, 40, 40, 0.8);
                border-radius: 50px;
                color: rgba(210, 210, 210, 0.8);
                border: 0px solid rgba(70, 70, 70, 0.8);
                margin-bottom: 2px;
            }
            QToolButton:pressed {
                background-color: rgba(60, 60, 60, 0.9);
                color: rgba(222, 222, 222, 1);                       
            }
            QToolButton:hover {
                background-color: rgba(60, 60, 60, 1);
                color: rgba(235, 235, 235, 0.9);
            }
            QToolButton:checked {
                background-color: rgba(40, 40, 40, 0.8);
                color: rgba(240, 240, 240, 0.9);
            }
            QToolButton:checked:pressed {
                background-color: rgba(60, 60, 60, 0.9);
                color: rgba(235, 235, 235, 0.9);
            }
            QToolButton:checked:hover {
                background-color: rgba(60, 60, 60, 1);
                color: rgba(230, 230, 230, 0.9);
            }
            """)
        
    def widgets_small_screen_values(self):
        if hasattr(self, 'app_name_label'):
            self.app_name_label.setFont(QFont(self.poppins_font, 12))
            # rest of your code
            self.app_name_label.setMinimumSize(QSize(100, 200))
            self.app_name_label.setAlignment(Qt.AlignCenter)
            self.app_name_label.setStyleSheet("color: rgba(210, 210, 210, 1); margin-top: 20px; padding: 15px; margin-bottom: 20px; border: solid 0px;")

        # Timer small ui values
        self.timer_label.setFont(QFont(self.azeret_mono_font, 64))
        self.timer_label.setMinimumSize(QSize(100, 200))
        self.timer_label.setStyleSheet("margin-bottom: 90px; color: rgba(210, 210, 210, 1); background-color: rgba(0, 0, 0, 0); border: solid 0px;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        

        self.start_button.setFont(QFont(self.poppins_semi_bold_font, 12))
        self.start_button.setFixedWidth(175)
        self.start_button.setFixedHeight(80)
        self.start_button.setStyleSheet("""
            QToolButton {
                background-color: rgba(40, 40, 40, 0.8);
                border-radius: 30px;
                color: rgba(210, 210, 210, 0.8);
              
                margin-bottom: 20px;
           
                border: 0px solid rgba(70, 70, 70, 0.8);
            }
                       
            QToolButton:pressed {
                background-color: rgba(60, 60, 60, 0.9);
                color: rgba(222, 222, 222, 1);                       
            }
            QToolButton:hover {
                background-color: rgba(60, 60, 60, 1);
                color: rgba(235, 235, 235, 0.9);
            }
            QToolButton:checked {
                background-color: rgba(40, 40, 40, 0.8);
                color: rgba(240, 240, 240, 0.9);
            }
            QToolButton:checked:pressed {
                background-color: rgba(60, 60, 60, 0.9);
                color: rgba(235, 235, 235, 0.9);
            }
            QToolButton:checked:hover {
                background-color: rgba(60, 60, 60, 1);
                color: rgba(230, 230, 230, 0.9);
            }
            """)
        
    def widgets_minimum_size_values(self):
         # Timer App small ui values
        self.app_name_label.setFont(QFont(self.poppins_font, 9))
        self.app_name_label.setMinimumSize(QSize(75, 40))
        self.app_name_label.setAlignment(Qt.AlignCenter)
        self.app_name_label.setStyleSheet("color: rgba(210, 210, 210, 1); margin-top: 0px; padding: 0 px; margin-bottom: 0px; border: solid 0px;")

        # Timer minimum ui values
        self.timer_label.setFont(QFont(self.azeret_mono_font, 19))
        self.timer_label.setMinimumSize(QSize(100, 200))
        self.timer_label.setStyleSheet("margin-bottom: 170px; margin-top: 0px; color: rgba(210, 210, 210, 1); background-color: rgba(0, 0, 0, 0); border: solid 0px;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        

        self.start_button.setFont(QFont(self.poppins_semi_bold_font, 7))
        self.start_button.setFixedWidth(75)
        self.start_button.setFixedHeight(50)
        self.start_button.setStyleSheet("""
            QToolButton {
                background-color: rgba(40, 40, 40, 0.8);
                border-radius: 10px;
                color: rgba(210, 210, 210, 0.8);
                margin-bottom: 20px;
                margin-top: 5px;
                border: 0px solid rgba(70, 70, 70, 0.8);
                
            }
              QToolButton:pressed {
                background-color: rgba(60, 60, 60, 0.9);
                color: rgba(222, 222, 222, 1);                       
            }
            QToolButton:hover {
                background-color: rgba(60, 60, 60, 1);
                color: rgba(235, 235, 235, 0.9);
            }
            QToolButton:checked {
                background-color: rgba(40, 40, 40, 0.8);
                color: rgba(240, 240, 240, 0.9);
            }
            QToolButton:checked:pressed {
                background-color: rgba(60, 60, 60, 0.9);
                color: rgba(235, 235, 235, 0.9);
            }
            QToolButton:checked:hover {
                background-color: rgba(60, 60, 60, 1);
                color: rgba(230, 230, 230, 0.9);
            }
            """)
        
    # Check window size, for responsive design
    def updateUI(self):
        # Example of responsive design
     
        width = self.width()
        height = self.height()

        if width < 750 or height < 475:

            self.widgets_small_screen_values()
        
            if width < 450 or height < 300:

                self.widgets_minimum_size_values()
        else:
            self.widgets_initial_values()
        
        if self.isMaximized():
            self.setStyleSheet("""
                        background-color: rgba(25, 25, 25, 1); 
                        border-radius: 0px;
                        border: 0px solid rgba(50, 50, 50, 1);
                        """)
        else:
            self.setStyleSheet("""
                        background-color: rgba(25, 25, 25, 1); 
                        border-radius: 10px;
                        border: 2px solid rgba(50, 50, 50, 1);
                        """)
    
    def toggleMaximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def eventFilter(self, source, event):
        if event.type() == QEvent.HoverMove:
            rect = self.rect()
            x = event.pos().x()
            y = event.pos().y()
            if rect.topLeft().y() + 10 >= y >= rect.topLeft().y() - 10 and rect.topLeft().x() + 10 >= x >= rect.topLeft().x() - 10:
                self.setCursor(Qt.SizeFDiagCursor)
            elif rect.bottomLeft().y() - 10 <= y <= rect.bottomLeft().y() + 10 and rect.bottomLeft().x() + 10 >= x >= rect.bottomLeft().x() - 10:
                self.setCursor(Qt.SizeBDiagCursor)
    
            elif rect.bottomRight().y() - 10 <= y <= rect.bottomRight().y() + 10 and rect.bottomRight().x() - 10 <= x <= rect.bottomRight().x() + 10:
                self.setCursor(Qt.SizeFDiagCursor)
            elif rect.topLeft().y() + 10 >= y >= rect.topLeft().y() - 10 or rect.bottomLeft().y() - 10 <= y <= rect.bottomLeft().y() + 10:
                self.setCursor(Qt.SizeVerCursor)
            elif rect.topLeft().x() + 10 >= x >= rect.topLeft().x() - 10 or rect.topRight().x() - 10 <= x <= rect.topRight().x() + 10:
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        return super().eventFilter(source, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_mouse_down = True
            self.m_drag = False  # Initialize drag action as False
            self.m_old_pos = event.globalPosition().toPoint()
            # Check if the window is maximized
            if self.isMaximized():
                self.m_drag = True
                # Store the normal size and position of the window
                self.m_normal_geometry = self.normalGeometry()
            rect = self.rect()
            x = event.pos().x()
            y = event.pos().y()
            width = self.width()
            height = self.height()
            min_width, min_height = self.minimumSize().width(), self.minimumSize().height()
            max_width, max_height = self.maximumSize().width(), self.maximumSize().height()
            # Reset the resize action and direction

            # Check if the mouse is within the resize area
            if ((width > min_width and height > min_height) or 
                (width < max_width and height < max_height)):
                if rect.topLeft().y() + 10 >= y >= rect.topLeft().y() - 10 and rect.topLeft().x() + 10 >= x >= rect.topLeft().x() - 10:
                    self.m_resize = True
                    self.m_resize_direction = 'top-left'
                elif rect.bottomLeft().y() - 10 <= y <= rect.bottomLeft().y() + 10 and rect.bottomLeft().x() + 10 >= x >= rect.bottomLeft().x() - 10:
                    self.m_resize = True
                    self.m_resize_direction = 'bottom-left'
                elif rect.topRight().y() + 10 >= y >= rect.topRight().y() - 10 and rect.topRight().x() - 10 <= x <= rect.topRight().x() + 10:
                    self.m_resize = True
                    self.m_resize_direction = 'top-right'
                elif rect.bottomRight().y() - 10 <= y <= rect.bottomRight().y() + 10 and rect.bottomRight().x() - 10 <= x <= rect.bottomRight().x() + 10:
                    self.m_resize = True
                    self.m_resize_direction = 'bottom-right'
                elif rect.topLeft().y() + 10 >= y >= rect.topLeft().y() - 10:
                    self.m_resize = True
                    self.m_resize_direction = 'top'
                elif rect.bottomLeft().y() - 10 <= y <= rect.bottomLeft().y() + 10:
                    self.m_resize = True
                    self.m_resize_direction = 'bottom'
                elif rect.topLeft().x() + 10 >= x >= rect.topLeft().x() - 10:
                    self.m_resize = True
                    self.m_resize_direction = 'left'
                elif rect.topRight().x() - 10 <= x <= rect.topRight().x() + 10:
                    self.m_resize = True
                    self.m_resize_direction = 'right'
                else:
                    self.m_drag = True  # Set drag action as True when mouse is down but not resizing
            else:
                self.m_resize = False
                self.m_mouse_down = False
                self.m_drag = True
    
    # Load bool settings that persist within user session
    def load_settings(self):
        # Get the root directory of your project
        src_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(src_dir)

        # Join the root directory with 'settings.json'
        self.settings_file = os.path.join(root_dir, 'settings.json')

        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            # Default settings
            self.settings = {
                'minimized_to_tray': False,
                'added_to_startup': False,
                'startup_minimized_tray': False,
            }
            # Save the default settings to a new settings.json file
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)

        self.minimized_to_tray = self.settings.get('minimized_to_tray', False)
        self.added_to_startup = self.settings.get('added_to_startup', False)
        self.startup_minimized_tray = self.settings.get('startup_minimized_tray', False)


    def start_tracking(self):
        if self.start_button.isChecked():
            self.time_tracker.start()
            self.show_notification("Fofaya started")
            self.start_button.setText('Stop Tracking')
            self.startTrackingAction.setChecked(True)
            self.startTrackingAction.setText("Stop Tracking")
            self.init_clock = False
        else:
            self.time_tracker.stop()
            self.show_notification("Fofaya Stopped")
            self.start_button.setText('Start Tracking')
            self.startTrackingAction.setChecked(False)
            self.startTrackingAction.setText("Start Tracking")
    
    def toggle_tracking(self, checked):
        if self.startTrackingAction.isChecked():
            self.time_tracker.start()
            self.show_notification("Fofaya started")
            self.startTrackingAction.setText('Stop Tracking')
            self.start_button.setChecked(True)
            self.start_button.setText('Stop Tracking')
        else:
            self.time_tracker.stop()
            self.show_notification("Fofaya Stopped")
            self.startTrackingAction.setText('Start Tracking')
            self.start_button.setChecked(False)
            self.start_button.setText('Start Tracking')
    
    def reset_tracking(self, reset):
        if reset:
            self.time_tracker.stop()
            self.show_notification("Fofaya Reset")
            self.start_button.setText('Start Tracking')
            self.startTrackingAction.setChecked(False)
            self.startTrackingAction.setText("Start Tracking")

            self.time_tracker.start()
            self.startTrackingAction.setText('Stop Tracking')
            self.start_button.setChecked(True)
            self.start_button.setText('Stop Tracking')
    
    def tracking_onDemand(self):
        self.time_tracker.start()
        self.show_notification("Fofaya started")
        self.startTrackingAction.setText('Stop Tracking')
        self.start_button.setChecked(True)
        self.start_button.setText('Stop Tracking')
    
    def show_notification(self, message):
        # Create a QLabel
        self.label = QLabel()
        self.label.setText(message)  # Use HTML tags to increase the font size
        self.label.setFont(QFont(self.poppins_semi_bold_font, 13))
        self.label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
       
        self.label.setStyleSheet("background-color: rgba(30, 30, 30, 150); color: white; padding: 15px; border-radius: 15px;")  # Adjust the alpha value to make the background less transparent

        # Adjust the size of the label to fit the text
        self.label.adjustSize()

        # Get the screen size
        screen_geometry = QApplication.screens()[0].geometry()

        # Calculate the position for the label to be in the center top part of the screen
        x = (screen_geometry.width() - self.label.width()) / 2
        y = (screen_geometry.height() / 10) - 90  # Adjust this value to move the label higher

        # Move the label to the calculated position
        self.label.move(x, y)

        # Show the label
        self.label.show()

        # Use a QTimer to automatically close the label after 1600 ms
        QTimer.singleShot(1600, self.label.close)

    def idle_applications(self):
        print("idle_applications called")  # Debugging line

        # Get the current app
        current_app = self.time_tracker.get_current_app()

        # Print the current app for debugging
        print(f"Current app: {current_app}")

        # If the current app is "Idle", call idle_clock_startup
        if current_app == "Idle":
            self.idle_clock_startup()
        else:
            # Update the app name label and start the timer
            self.app_name_label.setText(current_app)
            if not self.start_button.isChecked():
                self.start_tracking()
        
    def update_labels(self, app_name, timer):
        self.app_name_label.setText(app_name)
        self.timer_label.setText(timer)

    # Mouse Drag condition
    def moveEvent(self, event_):
        if not self.m_drag:
            return
    
    # Mouse Resize condition
    def enableResize(self):
    
        self.m_resize = True
    
    # Grab window functionality
    def moveWindow(self, event):
        self.setCursor(Qt.ArrowCursor)
        delta = QPoint(event.globalPosition().toPoint() - self.m_old_pos)
        self.m_old_pos = event.globalPosition().toPoint()
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
    # Resize window functionality
    def resizeWindow(self, event):
        """
        Custom PyQt6 window resize function.

        Parameters:
        event (QMouseEvent): Mouse event triggering the resize.

        This function, triggered when a window edge or corner is grabbed, resizes the window based on mouse movement direction. 
        It respects minimumWidth and minimumHeight to prevent undesired resizing. If the resize direction matches a key in the
        'resize_directions' dictionary, the window geometry and cursor icon are updated accordingly.
        """
        resize_directions = {
            'top': (self.x(), event.globalPosition().y() if self.height() > self.minimumHeight() else self.y(), self.width(), max(self.minimumHeight(), self.y() + self.height() - event.globalPosition().y()), Qt.SizeVerCursor),
            'bottom': (self.x(), self.y(), self.width(), max(self.minimumHeight(), event.globalPosition().y() - self.y()), Qt.SizeVerCursor),
            'left': (min(event.globalPosition().x(), self.x() + self.width() - self.minimumWidth()), self.y(), max(self.minimumWidth(), self.x() + self.width() - event.globalPosition().x()), self.height(), Qt.SizeHorCursor),
            'right': (self.x(), self.y(), max(self.minimumWidth(), event.globalPosition().x() - self.x()), self.height(), Qt.SizeHorCursor),
            'top-left': (event.globalPosition().x() if self.width() > self.minimumWidth() else self.x(), event.globalPosition().y() if self.height() > self.minimumHeight() else self.y(), max(self.minimumWidth(), self.x() + self.width() - event.globalPosition().x()), max(self.minimumHeight(), self.y() + self.height() - event.globalPosition().y()), Qt.SizeFDiagCursor),
            'bottom-left': (event.globalPosition().x() if self.width() > self.minimumWidth() else self.x(), self.y(), max(self.minimumWidth(), self.x() + self.width() - event.globalPosition().x()), max(self.minimumHeight(), event.globalPosition().y() - self.y()), Qt.SizeBDiagCursor),
            'bottom-right': (self.x(), self.y(), max(self.minimumWidth(), event.globalPosition().x() - self.x()), max(self.minimumHeight(), event.globalPosition().y() - self.y()), Qt.SizeFDiagCursor)
        }

        if self.m_resize_direction in resize_directions:
            self.setGeometry(*resize_directions[self.m_resize_direction][:4])
            self.setCursor(resize_directions[self.m_resize_direction][4])

    # Call mouse movement events, drag and resize
    def mouseMoveEvent(self, event):
        if self.m_mouse_down:

            if self.isMaximized():  # Check if the window is maximized
                self.showNormal()   # Restores window size to normal

            if self.m_drag:             # Check if the window can be dragged
                self.moveWindow(event)  # Call the moveWindow function

            if self.m_resize and self.cursor().shape() in [Qt.SizeVerCursor, Qt.SizeHorCursor, Qt.SizeFDiagCursor, Qt.SizeBDiagCursor]:
                self.m_drag = False
                self.resizeWindow(event)

    # Mouse release event, reset mouse boolean conditions
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_mouse_down = False
            self.m_drag = False
            self.m_resize = False
            self.m_resize_direction = None

    def resizeEvent(self, event):
        self.updateUI()
        super().resizeEvent(event)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        contextMenu.setTitle("Fofaya")

        # Set the stylesheet for the context menu
        contextMenu.setStyleSheet("""
            QMenu {
                background-color: rgba(30, 30, 30, 0.9); /* lighter gray */
                color: rgba(140, 140, 140, 1); /* gray text */
                border: 0px solid rgba(70, 70, 70, 0.8);
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: rgba(30, 30, 30, 0.9); /* lighter gray */
                color: rgba(230, 230, 230, 1); /* white text on selection */
            }
            QMenu::item:hover {
                background-color: rgba(30, 30, 30, 0.9); /* lighter gray */
                color: rgba(240, 240, 240, 1); /* white text on hover */
            }              
            QMenu::separator {
                height: 4px; /* make it more visible */
                background: rgba(35, 35, 35, 0.9); /* dark gray */
                margin: 6px 0; /* add some vertical spacing */
                border-radius: 2px; /* rounded corners */
            }
        """)

        alwaysOnTopAction = QAction("Always On Top", self, checkable=True)
        alwaysOnTopAction.setChecked(self.windowFlags() & Qt.WindowStaysOnTopHint)
        alwaysOnTopAction.triggered.connect(self.toggleAlwaysOnTop)
        alwaysOnTopAction.setToolTip("Keep on top of other windows")
        contextMenu.addAction(alwaysOnTopAction)
      

        # Add a separator to the context menu
        contextMenu.addSeparator()

        # Create the logs Window action
        logsAction = QAction("View App Time Logs", self)
        logsAction.triggered.connect(self.showLogs)  # Connect to the method that shows the logs
        logsAction.setToolTip("Opens usage data window")
        contextMenu.addAction(logsAction)
      
        # Create the logs Window action
        logsManagerAction = QAction("Manage Logs Data", self)
        logsManagerAction.setToolTip("Opens usage data manager window")
        logsManagerAction.triggered.connect(self.showLogsManger)  # Connect to the method that shows the logs
        contextMenu.addAction(logsManagerAction)

        # Add a separator to the context menu
        contextMenu.addSeparator()

        # Create the system tray action
        trayAction = QAction("Toggle Tray Minimize", self, checkable=True)
        trayAction.setChecked(self.minimized_to_tray)
        trayAction.triggered.connect(self.toggleMinimizeToTray)
        trayAction.setToolTip("On: Minize button hides to tray\nOff: Minimize to taksbar")
        contextMenu.addAction(trayAction)

        # Create the system tray action
        startTrayAction = QAction("Start Minimized To Tray", self, checkable=True)
        startTrayAction.setChecked(self.startup_minimized_tray)
        startTrayAction.triggered.connect(self.toggleStartMinimized)
        startTrayAction.setToolTip("Start minimized to tray")
        contextMenu.addAction(startTrayAction)

         # Add a separator to the context menu
        contextMenu.addSeparator()

        # Create the startup in system tray action
        startupAction = QAction("Start With System", self, checkable=True)
        startupAction.setChecked(self.added_to_startup)
        startupAction.triggered.connect(self.toggleAddToStartup)
        startupAction.setToolTip("Start with system")
        contextMenu.addAction(startupAction)

        
        # Add a separator to the context menu
        contextMenu.addSeparator()

        contextMenu.exec_(self.mapToGlobal(event.pos()))

    def toggleAddToStartup(self):
        if self.added_to_startup:
            self.added_to_startup = False
            # Remove the application from startup
            # You need to implement this method
            self.remove_from_startup()
        else:
            self.added_to_startup = True
            # Add the application to startup
            self.add_to_startup()
        # Save the state to settings
        self.settings_data.settings['added_to_startup'] = self.added_to_startup
        self.settings_data.save_settings()

    def toggleMinimizeToTray(self):
        if self.minimized_to_tray:
            self.minimized_to_tray = False
        else:
            self.minimized_to_tray = True
        # Save the state to settings
        self.settings_data.settings['minimized_to_tray'] = self.minimized_to_tray
        self.settings_data.save_settings()
    
    def toggleStartMinimized(self):
        if self.startup_minimized_tray:
            self.startup_minimized_tray = False
        else:
            self.startup_minimized_tray = True
        
        # Save the state to settings
        self.settings_data.settings['startup_minimized_tray'] = self.startup_minimized_tray
        self.settings_data.save_settings()
    
    def minimizeToTray(self):
        self.hide()
        self.trayIcon.show()

    def showLogsManger(self):
        # Import LogsWindow here to avoid circular import
        from src.excluded_apps_ui import ExcludedAppsWindow

        # Delete the old excluded apps window if it exists
        if hasattr(self, 'excluded_apps'):
            self.excluded_apps.deleteLater()

        # Create a new logs window
        self.excluded_apps = ExcludedAppsWindow(time_tracker=self.time_tracker, settings_data=self.settings_data)

        # Show the logs window
        self.excluded_apps.show()
    
    def showLogs(self):
        # Import LogsWindow here to avoid circular import
        from src.logs_window_ui import ChartWindow

        # Delete the old logs window if it exists
        if hasattr(self, 'logs_window'):
            self.logs_window.deleteLater()

        # Create a new logs window
        self.logs_window = ChartWindow(time_tracker=self.time_tracker, settings_data=self.settings_data)

        # Show the logs window
        self.logs_window.show()

    def toggleAlwaysOnTop(self, checked):
        # Block signals
        self.blockSignals(True)

        # Save the current size and position of the window
        current_geometry = self.geometry()
        size = QSize(current_geometry.width(), current_geometry.height())
        position = current_geometry.topLeft()

        # Toggle the "Always on Top" flag
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Window)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint | Qt.Window)

        # Show the window
        self.showNormal()

        # Set the position and size of the window after a delay
        QTimer.singleShot(200, lambda: self.move(position))
        QTimer.singleShot(200, lambda: self.resize(size))

        # Unblock signals
        self.blockSignals(False)
    
    def animateShow(self):
        # Start the animation from a small rectangle at the bottom of the screen
        startRect = QRect(self.geometry().x(), self.geometry().y() + self.geometry().height(), self.geometry().width(), 0)
        self.animation.setStartValue(startRect)
        self.animation.setEndValue(self.geometry())
        self.animation.start()
        self.normalGeometry = self.geometry()

    def showEvent(self, event):
        self.animateShow()

    def hideEvent(self, event):
        self.animateShow()

    def close_window(self):
        # Close the logs window and the excluded apps window if they exist
        if hasattr(self, 'logs_window'):
            self.logs_window.close()
        if hasattr(self, 'excluded_apps'):
            self.excluded_apps.close() 

        # Close the window after the animation has started
        self.close()
    
    def hideWindow(self):
        # This slot is called when the animation is finished
        if self.windowState() & Qt.WindowMinimized:
            # The window is minimized, so set its visibility to false
            self.setVisible(False)
        else:
            # The window is not minimized, so restore the normal geometry
            self.setGeometry(self.normalGeometry)
    
    def minimize(self):
        if self.minimized_to_tray:
            self.minimizeToTray()
        
        else:
            self.showMinimized()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            self.activateWindow()


