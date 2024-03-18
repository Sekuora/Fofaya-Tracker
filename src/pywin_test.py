import pygetwindow as gw

# Get the currently active window
active_window = gw.getActiveWindow()

# Get the title of the active window
window_title = active_window.title

# Print the window title
print(f"The active window's title is: {window_title}")