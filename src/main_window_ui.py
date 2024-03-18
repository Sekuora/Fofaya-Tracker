from PySide6.QtWidgets import QMainWindow, QWidgetAction, QLabel, QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QSystemTrayIcon, QMenu, QApplication, QSpacerItem
from PySide6.QtGui import QPalette, QColor, QFont, QIcon, QAction, QPainter, QBrush
from PySide6.QtCore import Qt, QSize, QPoint, QEvent, QTimer, QPropertyAnimation, QEasingCurve, QRect
import sys
import os


class CustomMenu(QMenu):
    def mouseMoveEvent(self, event):
        if not self.geometry().adjusted(-50, -50, 50, 50).contains(event.globalPos()):
            self.close()
        super().mouseMoveEvent(event)

class MainWindow(QMainWindow):
    def __init__(self, tracker):

        super().__init__()

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

        # Set the icon for the tray
    

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

 
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(25)  # Set the height to 30 pixels
        close_button.setFixedWidth(35)  # Set the width to 30 pixels
        close_button.setIconSize(QSize(25, 25))
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
        maximize_button.setFixedHeight(25)  # Set the height to 30 pixels
        maximize_button.setFixedWidth(35)  # Set the width to 30 pixels
        maximize_button.setIconSize(QSize(25, 25))
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
       
        minimize_button.clicked.connect(self.showMinimized)
        minimize_button.setFixedHeight(25)  # Set the height to 30 pixels
        minimize_button.setFixedWidth(35)  # Set the width to 30 pixels
        minimize_button.setIconSize(QSize(25, 25))
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
        self.resize(1280, 720)
        self.setMinimumSize(200, 150)
        self.setMaximumSize(1920, 1080)
        # Set the background color to a semi-transparent white
        self.setStyleSheet("""
                            background-color: rgba(30, 30, 30, 0.99); 
                            border-radius: 10px;
                            border: 2px solid rgba(50, 50, 50, 0.8);
                            """)
        
        self.m_mouse_down = False
        self.m_resize = False
        self.m_resize_direction = None

    def widgets_initial_values(self):
        if hasattr(self, 'app_name_label'):
            self.app_name_label.setFont(QFont("Poppins Regular", 19))
            self.app_name_label.setMinimumSize(QSize(100, 200))
            self.app_name_label.setAlignment(Qt.AlignCenter)
            self.app_name_label.setStyleSheet("""
                                            color: rgba(170, 170, 170, 0.9);
                                            margin-top: 125px; padding: 15px;
                                            margin-bottom: 0px;
                                            margin-right: 2px;
                                            margin-left: 2px;
                                            border: 0px solid rgba(70, 70, 70, 0.8);
                                            """)

        # Timer init values
        self.timer_label.setFont(QFont("Azeret Mono Medium", 95))
        self.timer_label.setMinimumSize(QSize(100, 200))
        self.timer_label.setStyleSheet("margin-bottom: 40px; color: rgba(170, 170, 170, 0.9); background-color: rgba(0, 0, 0, 0); border: solid 0px;")
        self.timer_label.setAlignment(Qt.AlignCenter)

        # Start Tracking Button init values
        self.start_button.clicked.connect(self.start_tracking)
        self.start_button.setFont(QFont("Poppins Semibold", 24))
        self.start_button.setFixedWidth(300)
        self.start_button.setFixedHeight(105)
        self.start_button.setCheckable(True)
        self.start_button.setStyleSheet("""
            QToolButton {
                background-color: rgba(43, 43, 43, 0.7);
                border-radius: 50px;
                color: rgba(210, 210, 210, 0.8);
                border: 0px solid rgba(70, 70, 70, 0.8);
            
                margin-bottom: 2px;
                
                
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
            """)
        
    def widgets_small_screen_values(self):
        if hasattr(self, 'app_name_label'):
            self.app_name_label.setFont(QFont("Poppins Regular", 12))
            # rest of your code
            self.app_name_label.setMinimumSize(QSize(100, 200))
            self.app_name_label.setAlignment(Qt.AlignCenter)
            self.app_name_label.setStyleSheet("color: rgba(170, 170, 170, 0.9); margin-top: 20px; padding: 15px; margin-bottom: 20px; border: solid 0px;")

        # Timer small ui values
        self.timer_label.setFont(QFont("Azeret Mono Medium", 64))
        self.timer_label.setMinimumSize(QSize(100, 200))
        self.timer_label.setStyleSheet("margin-bottom: 90px; color: rgba(170, 170, 170, 0.9); background-color: rgba(0, 0, 0, 0); border: solid 0px;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        

        self.start_button.setFont(QFont("Poppins Semibold", 12))
        self.start_button.setFixedWidth(175)
        self.start_button.setFixedHeight(80)
        self.start_button.setStyleSheet("""
            QToolButton {
                background-color: rgba(43, 43, 43, 0.7);
                border-radius: 30px;
                color: rgba(210, 210, 210, 0.8);
              
                margin-bottom: 20px;
           
                border: 0px solid rgba(70, 70, 70, 0.8);
            }
            QToolButton:pressed {
                background-color: rgba(47, 47, 47, 0.7);
                color: rgba(232, 232, 232, 1);                     
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
                color: rgba(240, 240, 240, 0.9);
            }
            """)
        
    def widgets_minimum_size_values(self):
         # Timer App small ui values
        self.app_name_label.setFont(QFont("Poppins Regular", 9))
        self.app_name_label.setMinimumSize(QSize(75, 40))
        self.app_name_label.setAlignment(Qt.AlignCenter)
        self.app_name_label.setStyleSheet("color: rgba(170, 170, 170, 0.9); margin-top: 0px; padding: 0 px; margin-bottom: 0px; border: solid 0px;")

        # Timer minimum ui values
        self.timer_label.setFont(QFont("Azeret Mono Medium", 24))
        self.timer_label.setMinimumSize(QSize(100, 200))
        self.timer_label.setStyleSheet("margin-bottom: 170px; margin-top: 0px; color: rgba(170, 170, 170, 0.9); background-color: rgba(0, 0, 0, 0); border: solid 0px;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        

        self.start_button.setFont(QFont("Poppins Semibold", 7))
        self.start_button.setFixedWidth(85)
        self.start_button.setFixedHeight(60)
        self.start_button.setStyleSheet("""
            QToolButton {
                background-color: rgba(43, 43, 43, 0.7);
                border-radius: 10px;
                color: rgba(210, 210, 210, 0.8);
                margin-bottom: 25px;
                margin-top: 10px;
                border: 0px solid rgba(70, 70, 70, 0.8);
                
            }
            QToolButton:pressed {
                background-color: rgba(47, 47, 47, 0.7);
                color: rgba(232, 232, 232, 1);                      
            }
            QToolButton:hover {
                background-color: rgba(45, 45, 45, 0.7);
                color: rgba(232, 232, 232, 0.9);
            }
            
            QToolButton:checked {
                background-color: rgba(44, 44, 44, 0.7);
                color: rgba(220, 220, 220, 0.9);
            }
            QToolButton:checked:pressed {
                background-color: rgba(51, 51, 51, 0.7);
                color: rgba(222, 222, 222, 0.8);
            }
            QToolButton:checked:hover {
                background-color: rgba(45, 45, 45, 0.7);
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
                        background-color: rgba(30, 30, 30, 0.99); 
                        border-radius: 0px;
                        border: 0px solid rgba(50, 50, 50, 0.8);
                        """)
        else:
            self.setStyleSheet("""
                        background-color: rgba(30, 30, 30, 0.99); 
                        border-radius: 10px;
                        border: 2px solid rgba(50, 50, 50, 0.8);
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
    
    def start_tracking(self):
        if self.start_button.isChecked():
            self.time_tracker.start()
            self.start_button.setText('Stop Tracking')
            self.init_clock = False
        else:
            self.time_tracker.stop()
            self.start_button.setText('Start Tracking')
        
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
                background-color: rgba(40, 40, 40, 0.9); /* lighter gray */
                color: rgba(140, 140, 140, 1); /* gray text */
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: rgba(50, 50, 50, 0.9); /* lighter gray */
                color: rgba(210, 210, 210, 1); /* white text on selection */
            }
            QMenu::item:hover {
                background-color: rgba(60, 60, 60, 0.9); /* lighter gray */
                color: rgba(240, 240, 240, 1); /* white text on hover */
            }
        """)

        alwaysOnTopAction = QAction("Always on Top", self, checkable=True)
        alwaysOnTopAction.setChecked(self.windowFlags() & Qt.WindowStaysOnTopHint)
        alwaysOnTopAction.triggered.connect(self.toggleAlwaysOnTop)
        contextMenu.addAction(alwaysOnTopAction)

        # Create the logs action
        logsAction = QAction("Open Logs", self)
        logsAction.triggered.connect(self.showLogs)  # Connect to the method that shows the logs
        contextMenu.addAction(logsAction)

        # Create the system tray action
        trayAction = QAction("System Tray", self)
        trayAction.triggered.connect(self.minimizeToTray)
        contextMenu.addAction(trayAction)


        contextMenu.exec_(self.mapToGlobal(event.pos()))
    
    def minimizeToTray(self):
        self.hide()
        self.trayIcon.show()
    
    def showLogs(self):

        # Import LogsWindow here to avoid circular import
        from src.logs_window_ui import ChartWindow

        # Delete the old logs window if it exists
        if hasattr(self, 'logs_window'):
            self.logs_window.deleteLater()

        # Create a new logs window
        self.logs_window = ChartWindow(time_tracker=self.time_tracker)

        # Show the logs window
        self.logs_window.show()

    def showExcludedApps(self):
        # Import LogsWindow here to avoid circular import
        from src.excluded_apps_ui import ExcludedAppsWindow
   

        # Delete the old logs window if it exists
        if hasattr(self, 'excluded_apps_window'):
            self.excluded_apps_window.deleteLater()

        # Create a new logs window
        self.excluded_apps_window = ExcludedAppsWindow(time_tracker=self.time_tracker)

        # Show the logs window
        self.excluded_apps_window.show()

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

    def closeEvent(self, event):

        self.time_tracker.stop()
        if hasattr(self, 'logs_window'):
            self.logs_window.close()
        if hasattr(self, 'excluded_apps_window'):
            self.excluded_apps_window.close()   

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
        

        self.showMinimized()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isMinimized():
                self.showNormal()
            else:
                self.showMinimized()

