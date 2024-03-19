[Video of the Fofaya](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

# Fofaya Tracker
This is my first application project in Python, But I've been using Python for around 4-5 months now.
This app is a Time Tracker that monitors the time spent on different applications on a Windows machine. This project was developed with the assistance of GitHub Copilot, an AI-powered code completion tool.

## Project Description
The Time Tracker is a Python application that uses the PySide6.QtCore, psutil, win32process, win32gui, and pygetwindow libraries to track the active application on a Windows machine and record the time spent on each application.

The code is a bit messy and could be improved. I am considering working on that, but as the application already works with most of the features I wanted, I don't plan on making significant changes in the near future.

## Installation
There are two ways to install the Time Tracker:

1. Installer: Download the installer from the releases section and follow the installation prompts.

2. ZIP File: Download the ZIP file from the releases section, extract the files, and run the main script.

## Usage
1. Start Tracking: After installation, run the application. You just need to press the start tracking button.
   
2. Idle: Idle clock will be turned on by default when the app is the tracker itself and when checking windows   
   services
   
3. Context Menu: With right-click you can acess the context menu and its feature:
   - Always on top: Makes sure the app is visible on top of other applications, except in full-screen applications
   - Open Logs: The main way to check the logged data from the tracker.
   - System Tray: Makes the app run on the background. With right-click on tray icon you re-open the app.

4. Logs Window: The logs window allows to visualize the data gathered from the tracker. It is in a scale of 16 hours,
   as it is intended for productivity I considered the max to be 16 hours a day. Through the calendar widget you can 
   choose which day to show in the graphs. And in filters, currently you can only filter the total time spent on 
   every app.

## Contributions
As this is my first Python project, I welcome any suggestions or contributions to improve the code or add new features. Please feel free to open an issue or submit a pull request.

## Acknowledgements
I would like to thank GitHub Copilot for assisting me in this project. The AI-powered code completion tool was invaluable in helping me navigate the Python language and libraries.

## License
This project is open source and available under the MIT License.


