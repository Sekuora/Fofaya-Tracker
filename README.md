[Video of the Fofaya](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

# Fofaya Tracker
This is my first application project in Python, But I've been using Python for around 4-5 months now.
This app is a Time Tracker that monitors the time spent on different applications on a Windows machine. This project was developed with the assistance of GitHub Copilot, an AI-powered code completion tool.

## Project Description
The Fofaya Tracker is a Python application that uses the PySide6.QtCore, psutil, win32process, win32gui, and pygetwindow libraries to track the active application on a Windows machine and record the time spent on each application.

The code is a bit messy and could be improved.

## Installation

**Installer:** Download the installer from the releases section and follow the installation prompts.

## Usage
**1. Start Tracking:** After installation, run the application. You just need to press the start tracking button.
   
**2. Idle:** Idle clock will be turned on by default when the app is the tracker itself and when checking windows   
   services
   
**3. Context Menu:** With right-click you can acess the context menu and its feature:
   - Always on top: Makes sure the app is visible on top of other applications, except in full-screen applications
   - Open Logs: The main way to check the logged data from the tracker.
   - System Tray: Makes the app run on the background. With right-click on tray icon you re-open the app.

**4. Logs Window:** 
The logs window allows to visualize the data gathered from the tracker. It is in a scale of 16 hours,
as it is intended for productivity I considered the max to be 16 hours a day. Through the calendar widget you can 
choose which day to show in the graphs. And in filters, currently you can only filter the total time spent on 
every app.

## Compile Instructions

1. Ensure Python 3.x is installed on your system.
2. Optionally, create a virtual environment.
3. Install the required libraries by running the following command in your terminal:
    ```bash
    pip install -r requirements.txt
    ```
4. PyInstaller is included in the requirements and it is what I used to compile the program.
5. Compile the program with the following command:
    ```bash
    pyinstaller app.spec
    ```
6. The compiled program will be in the `dist` directory.


## Contributions
I welcome any suggestions or contributions from more experienced developers to improve the code or add new features. Please feel free to open an issue or submit a pull request.

## Acknowledgements
I would like to thank GitHub Copilot for assisting me in this project. The AI-powered code completion tool was invaluable in helping me navigate the Python language and libraries.

## License
This project is open source and available under the GPL-3.0 license.



