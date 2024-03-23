# log_window_ui.py
# Copyright (C) 2024 Sekuora
# This file is part of a software tool distributed under the GNU General Public License.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import json
from collections import defaultdict
import math

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as fm


from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QTextCharFormat, QAction, QIcon
from PySide6.QtWidgets import (QHBoxLayout, 
                               QPushButton, QVBoxLayout, QWidget, 
                               QCalendarWidget, QToolButton, QMenu, 
                               QWidgetAction)

from .main_window_ui import MainWindow
import os

class ChartWindow(MainWindow):
    def __init__(self, time_tracker, settings_data=None):
        super().__init__(tracker=time_tracker, settings_data=settings_data)
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Build the paths to the font files
        self.poppins_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'Poppins-Medium.ttf')
        self.azeret_mono_font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'AzeretMono-Regular.ttf')

        # Load 'Poppins' font
        self.poppins_font = fm.FontProperties(fname=self.poppins_font_path)

        # Load 'Azeret Mono' font
        self.azeret_mono_font = fm.FontProperties(fname=self.azeret_mono_font_path)
        # Initialize current_page
        self.current_page = 0

        self.get_icons_path()

        self.view_mode = 'date'
      
        self.set_initial_values()
        top_bar_widget = self.top_bar()

        self.tracker = time_tracker
        self.calendar_style = """
            QCalendarWidget {
                background-color: rgba(40, 40, 40, 1);
                color: rgb(170, 170, 170);
                selection-background-color: rgb(0, 0, 170);
                selection-color: rgb(255, 255, 255);
            }
            QCalendarWidget QWidget {
                alternate-background-color: rgb(100, 100, 102);
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 12px;
                color: rgb(150, 150, 150);
                background-color: rgb(40, 40, 40);
                selection-background-color: rgba(55, 55, 55, 0.8);
                selection-color: rgb(120, 120, 120);  /* Changed here */
            }
            QCalendarWidget QMenu {
                color: rgb(255, 255, 255);
            }
            QCalendarWidget QMenu::item {
                color: rgb(175, 175, 175);
            }
        """
        # Create a QTextCharFormat object for weekend dates
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QColor(150, 150, 150))

        self.Menu_style = """
            QMenu {
                background-color: rgba(43, 43, 43, 0.7);
                color: rgba(210, 210, 210, 0.8);
                border: 1px solid rgba(70, 70, 70, 0.8);
                margin: 2px;
                border-radius: 5px;
            }
            QMenu::item {
                padding: 2px 20px 2px 20px;
            }
            QMenu::item:selected {
                background-color: rgba(45, 45, 45, 0.7);
                color: rgba(230, 230, 230, 0.9);
            }
        """

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
        # Create a new QToolButton
        self.filter_button = QToolButton(self)
        self.filter_button.setPopupMode(QToolButton.InstantPopup)
        self.filter_button.setText('Filters')
        self.filter_button.setStyleSheet(self.Toolbutton_style)

            # Create a new QMenu
        self.filter_menu = QMenu(self)
        self.filter_menu.setStyleSheet(self.Menu_style)

        # Set the menu for the button
        self.filter_button.setMenu(self.filter_menu)

        # Create a new QAction
        most_used_all_time_action = QAction('Most Used Apps All Time', self)
        
        # Add the action to the filter_menu
        self.filter_menu.addAction(most_used_all_time_action)

       
        # Connect the action to the filter_charts function
        most_used_all_time_action.triggered.connect(lambda: self.all_time_mode('Most Used Apps All Time'))

        # Create a calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(350, 350)
        self.calendar.setStyleSheet(self.calendar_style)
        self.calendar.selectionChanged.connect(self.on_date_selected)

        
        # Apply the format to weekend dates
        self.calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)

        # Create a layout for the buttons
        self.button_layout = QHBoxLayout()

        # Create a layout and add the canvas to it
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2, 0, 2, 10)
        # Add the top bar widget to the layout
        self.layout.addWidget(top_bar_widget)
        
        self.toggle_calendar_button = QToolButton()
        self.toggle_calendar_button.setText("Calendar")
        self.toggle_calendar_button.setStyleSheet(self.Toolbutton_style)

        # Create a menu for the tool button
        self.calendar_menu = QMenu(self.toggle_calendar_button)

        # Add the calendar to the menu as a widget action
        calendar_action = QWidgetAction(self.calendar_menu)
        calendar_action.setDefaultWidget(self.calendar)
        self.calendar_menu.addAction(calendar_action)

        # Set the menu for the tool button
        self.toggle_calendar_button.setMenu(self.calendar_menu)
        self.toggle_calendar_button.setPopupMode(QToolButton.InstantPopup)

        # Add the button to the layout
        self.button_layout.addWidget(self.toggle_calendar_button)

        # Add the button to the layout
        self.layout.addWidget(self.filter_button)

        top_bar_widget.setStyleSheet("background-color: rgba(40, 40, 40, 0.15); border: 0px solid rgba(70, 70, 70, 0.8); border-bottom: 0px solid rgba(70, 70, 70, 0.8);")  # 0.8 for 80% opacity

        self.button_style = ("""
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
            """)

        plt.rcParams['figure.facecolor'] = (30/255, 30/255, 30/255, 0.99)

        self.setStyleSheet("""
                    background-color: rgba(30, 30, 30, 0.99); 
                    border-radius: 10px;
                    border: 2px solid rgba(50, 50, 50, 0.8);
                    """)

        # Initialize start and end
        self.start = 0
        self.end = 3

        # Create buttons
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet(self.button_style)
        self.prev_button = QPushButton("Previous")
        self.prev_button.setStyleSheet(self.button_style)

        # Connect buttons to functions
        self.next_button.clicked.connect(self.next)
        self.prev_button.clicked.connect(self.prev)

        # Add the buttons to the layout
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        # Set the font size and family
        mpl.rcParams['font.size'] = 10
        mpl.rcParams['font.family'] = 'Poppins'
        mpl.rcParams['font.weight'] = 'semibold'

        # Create a figure and a canvas
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)

        # Add the canvas to the layout
        self.layout.addWidget(self.canvas)

        # Create a widget and set the layout to it
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        # Set the widget as the central widget of the window
        self.setCentralWidget(self.widget)

        # Create a timer
        self.timer = QTimer()
        self.timer_states(tracker =  self.tracker)
        

        # Initial chart update
        self.date_charts()


        self.setWindowIcon(QIcon(self.window_icon_path))

    
    def timer_states(self, tracker):
        # Disconnect the timer's timeout signal from all slots
        try:
            self.timer.timeout.disconnect()
        except RuntimeError:
            # Ignore the error if the signal was not connected to any slots
            pass

        # Only start the timer if on the first page
        if self.start == 0:
            if self.view_mode == 'date':
                self.timer.timeout.connect(self.date_charts)
                self.timer.start(10000)  # Update every 10 second
                tracker.data_updated.connect(self.date_charts)
                print(self.view_mode)
            elif self.view_mode == 'all_time':
                self.timer.timeout.connect(self.filter_charts)
                self.timer.start(10000)  # Update every 10 seconds
                tracker.data_updated.connect(self.filter_charts)
                print(self.view_mode)


    def all_time_mode(self, view_mode):
        self.view_mode = 'all_time'  # Set the view mode to 'all_time'

        self.filter_charts()

        if self.start == 0:
            self.timer.start(1000)  # Set timer interval to 1 second
            self.filter_charts()  # Update the chart immediately
            self.timer.start(10000)  # Set timer interval back to 10 seconds
            self.timer_states(tracker =  self.tracker)

        
    def on_date_selected(self):
        self.view_mode = 'date'  # Add this line

        self.date_charts()
        if self.start == 0:
            self.timer.start(1000)  # Set timer interval to 1 second
            self.date_charts()  # Update the chart immediately
            self.timer.start(10000)  # Set timer interval back to 10 seconds
            self.timer_states(tracker =  self.tracker)

 
        
    def toggle_calendar(self):
            # Toggle the visibility of the calendar menu
            self.calendar_menu.setVisible(not self.calendar_menu.isVisible())
            
    def next(self):
        # Stop the timer
        self.timer.stop()

        self.current_page += 1

       
        if self.view_mode == 'date':
            self.date_charts(self.start, self.end)
        elif self.view_mode == 'all_time':
            self.filter_charts(self.start, self.end)

    def prev(self):
        self.current_page = max(0, self.current_page - 1)  # Ensure current_page is not negative

    # Restart the timer if on the first page
        if self.current_page == 0:
            self.timer.start()

        if self.view_mode == 'date':
            self.date_charts()
        elif self.view_mode == 'all_time':
            self.filter_charts()

    def get_selected_date(self):
        # Assuming you have a QCalendarWidget named calendar
        selected_date = self.calendar.selectedDate()
        return selected_date.toString('dd/MM/yyyy')

    def date_charts(self, start=0, end=3):
        if self.view_mode != 'date':  # Add this line
            return  # Add this line
        
            # If start and end are None, use the current page
   
        start = self.current_page * 3
        end = start + 3
    
        plt.style.use('dark_background')
        # Load the data
        with open('app_times.json') as f:
            self.data = json.load(f)
        
        # Get the selected date from the calendar widget
        selected_date = self.get_selected_date()
        title_date = self.calendar.selectedDate().toString('MMMM d, yyyy')

        # Aggregate total time for each app for the selected date only
        total_times = defaultdict(int)
        for app, times in self.data.items():
            if selected_date in times:
                total_times[app] += times[selected_date]

        # Convert seconds to hours and prepare data for plotting
        apps = []
        times = []
        for app, total_time in sorted(total_times.items(), key=lambda item: item[1], reverse=True):
            if app != "Idle":
                apps.append(app)
                times.append(total_time / 3600)  # Convert seconds to hours

        # Clear the figure
        self.fig.clear()

        # Only plot the data if there are entries
        if apps[start:end] and times[start:end]:
            # Create a bar chart
            ax = self.fig.add_subplot(111)
            ax.set_facecolor((30/255, 30/255, 30/255))
            # Change the color and width of the spines
            for spine in ax.spines.values():
                spine.set_color((160/255, 160/255, 160/255, 1))  # Change the color to match the ticks
                spine.set_linewidth(0.5)  # Change the width as needed

            ax.tick_params(axis='x', colors=(160/255, 160/255, 160/255, 1))
            ax.tick_params(axis='y', colors=(160/255, 160/255, 160/255, 1))
            bars = ax.bar(apps[start:end], times[start:end])
            ax.set_ylabel('Usage Time (hours)', color=(160/255, 160/255, 160/255, 1))
            title_font = {'fontproperties': self.poppins_font, 'fontsize': 10, 'fontweight': 'medium', 'color': (160/255, 160/255, 160/255, 1)}
            ax.set_title('App Usage\n' + title_date, loc='center', color=(160/255, 160/255, 160/255, 1), fontdict=title_font)  # Set the selected date as the subtitle
            ax.set_ylim([0, 16])  # Set y-axis limits from 0 to 16 hours

            for bar in bars:
                bar.set_color((0/255, 100/255, 212/255, 1))  # Set the color of the bars to blue
                height = bar.get_height()  # height is in hours
                hours = int(height)
                minutes = int((height - hours) * 60)
                seconds = int((height - hours - minutes / 60) * 3600)
                label_font = {'fontproperties': self.azeret_mono_font, 'fontsize': 11, 'fontweight': 'bold', 'color': (170/255, 170/255, 170/255, 1)}
                ax.text(bar.get_x() + bar.get_width() / 2, height,
                        f'{hours:02d}:{minutes:02d}:{seconds:02d}', ha='center', va='bottom', color=(160/255, 160/255, 160/255, 1), 
                        fontdict=label_font)

            # Adjust the layout
            plt.tight_layout()

        # Disable the "Next" button if there are no more entries
        self.next_button.setEnabled(len(apps) > end)

        # Redraw the canvas
        self.canvas.draw()
    
    def filter_charts(self, start=0, end=3):
        if self.view_mode != 'all_time':  # Add this line
            return  # Add this line
        
        # If start and end are None, use the current page
       
        start = self.current_page * 3
        end = start + 3

        plt.style.use('dark_background')

        # Load the data
        with open('app_times.json') as f:
            self.data = json.load(f)

        # Aggregate total time for each app across all dates
        total_times = defaultdict(int)
        for app, times in self.data.items():
            for date, time in times.items():
                total_times[app] += time

        # Convert seconds to hours and prepare data for plotting
        apps = []
        times = []
        for app, total_time in sorted(total_times.items(), key=lambda item: item[1], reverse=True):  # Remove slicing here
            if app != "Idle":  # Skip the "Idle" entries
                apps.append(app)
                times.append(total_time / 3600)  # Convert seconds to hours

        # Clear the figure
        self.fig.clear()

        # Only plot the data if there are entries
        if apps[start:end] and times[start:end]:
            # Create a bar chart
            ax = self.fig.add_subplot(111)
            ax.set_facecolor((30/255, 30/255, 30/255))

            # Change the color and width of the spines
            for spine in ax.spines.values():
                spine.set_color((160/255, 160/255, 160/255, 1))  # Change the color to match the ticks
                spine.set_linewidth(0.5)  # Change the width as needed

            ax.tick_params(axis='x', colors=(160/255, 160/255, 160/255, 1))
            ax.tick_params(axis='y', colors=(160/255, 160/255, 160/255, 1))
            bars = ax.bar(apps[start:end], times[start:end])
            ax.set_ylabel('Usage Time (hours)', color=(160/255, 160/255, 160/255, 1))
            title_font = {'fontproperties': self.poppins_font, 'fontsize': 10, 'fontweight': 'medium', 'color': (160/255, 160/255, 160/255, 1)}
            ax.set_title('App Usage\n' + 'All Time', loc='center', color=(160/255, 160/255, 160/255, 1), fontdict=title_font)  # Set the selected date as the subtitle
            
            # Set y-axis limits from 0 to maximum time or 16 hours, whichever is greater
            max_time = max(times)
            ax.set_ylim([0, math.ceil(max_time)])

            for bar in bars:
                bar.set_color((0/255, 100/255, 212/255, 1))  # Set the color of the bars to blue
                height = bar.get_height()  # height is in hours
                hours = int(height)
                minutes = int((height - hours) * 60)
                seconds = int((height - hours - minutes / 60) * 3600)
                label_font = {'fontproperties': self.azeret_mono_font, 'fontsize': 11, 'fontweight': 'bold', 'color': (170/255, 170/255, 170/255, 1)}
                ax.text(bar.get_x() + bar.get_width() / 2, height,
                        f'{hours:02d}:{minutes:02d}:{seconds:02d}', ha='center', va='bottom', color=(160/255, 160/255, 160/255, 1), 
                        fontdict=label_font)

            # Adjust the layout
            plt.tight_layout()

        # Disable the "Next" button if there are no more entries
        self.next_button.setEnabled(len(apps) > end)

        # Redraw the canvas
        self.canvas.draw()

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
        self.setWindowTitle("Fofaya")
        self.resize(600, 400)
        self.setMinimumSize(600, 400)
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

        contextMenu.exec_(self.mapToGlobal(event.pos()))