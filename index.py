import tkinter as tk
from pynput import keyboard, mouse
from datetime import datetime
from threading import Thread
import webbrowser


'''
Define the name of the log file
where the activities will be recorded
'''
log_file = "activity_log.txt"


activity_log = []

"""
    Logs an activity with a timestamp.

    Args:
        action (str): A description of the action performed (e.g., "Key Press", "Mouse Click").
        detail (str, optional): Additional details about the action (e.g., which key was pressed).
"""
def log_activity(action, detail=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    activity_log.append(f"[{timestamp}] {action}: {detail}")

"""
    Writes the logged activities to a specified log file in reverse order.

    This function opens the log file in write mode and iterates over the
    activity_log list in reverse, writing each entry to the file. The 
    log file is overwritten each time logging is stopped, ensuring that 
    only the most recent actions are saved.
"""
def write_log_to_file():
    with open(log_file, "w") as f:
        for entry in reversed(activity_log):
            f.write(f"{entry}\n")

"""
    Handles keyboard key press events.
    Args:
        key (Key): The key that was pressed.
    This function attempts to log the pressed key as a character. If the key 
    is a special key (like Ctrl or Alt), it logs it differently.
"""
def on_key_press(key):
    try:
        log_activity("Key Press", key.char)
    except AttributeError:
        log_activity("Special Key Press", str(key))

"""
    Handles mouse move events.

    Args:
        x (int): The x-coordinate of the mouse pointer.
        y (int): The y-coordinate of the mouse pointer.

    This function logs the new position of the mouse pointer whenever it moves.
"""
def on_move(x, y):
    log_activity("Mouse Move", f"({x}, {y})")

"""
    Handles mouse click events.

    Args:
        x (int): The x-coordinate where the mouse was clicked.
        y (int): The y-coordinate where the mouse was clicked.
        button (Button): The mouse button that was pressed or released.
        pressed (bool): True if the button was pressed, False if released.

    This function logs whether the mouse button was pressed or released, along with its position.
"""
def on_click(x, y, button, pressed):
    action = "Mouse Click Pressed" if pressed else "Mouse Click Released"
    log_activity(action, f"{button} at ({x}, {y})")

"""
    Handles mouse scroll events.

    Args:
        x (int): The x-coordinate of the mouse during the scroll.
        y (int): The y-coordinate of the mouse during the scroll.
        dx (int): The horizontal scroll amount.
        dy (int): The vertical scroll amount.

    This function logs the scrolling action along with the amount and position.
"""
def on_scroll(x, y, dx, dy):
    log_activity("Mouse Scroll", f"({dx}, {dy}) at ({x}, {y})")


root = tk.Tk()
root.title("WD windows tracker")
root.geometry("300x150")
root.resizable(False, False)
keyboard_listener = None
mouse_listener = None

"""
    Initializes and starts the keyboard and mouse listeners in separate threads.
    
    This function creates instances of the keyboard and mouse listeners, 
    associating their events with the corresponding handler functions. 
    The listeners are then started in separate threads to allow them 
    to run concurrently with the GUI.
"""
def start_logging():
    global keyboard_listener, mouse_listener
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    Thread(target=keyboard_listener.start).start()
    Thread(target=mouse_listener.start).start()
    
    # hide the start button and show the other
    start_button.pack_forget()
    stop_button.pack(pady=10)

"""
    Stops the keyboard and mouse listeners and writes the logged activities to the log file.

    This function checks if the listeners are active, stops them, 
    and then calls the function to write the logged activities to the log file.
"""
def stop_logging():
    global keyboard_listener, mouse_listener
    if keyboard_listener is not None:
        keyboard_listener.stop()
    if mouse_listener is not None:
        mouse_listener.stop()

    write_log_to_file()
    
    # the opposite
    stop_button.pack_forget()
    start_button.pack(pady=10)
    
def open_website(event):
    webbrowser.open("https://wadiecoder.com")
    
start_button = tk.Button(root, text="Start Logging", command=start_logging, bg="green", fg="white")
stop_button = tk.Button(root, text="Stop Logging", command=stop_logging, bg="red", fg="white")

start_button.pack(pady=10)

credit_label = tk.Label(root, text="Made by Wadie Coder © "+ str(datetime.now().year), fg="blue", cursor="hand2")
credit_label.pack(side="bottom",pady=10)
credit_label.bind("<Button-1>", open_website)

root.mainloop()
