"""
Code by Aki,
Created on Sep.20, 2024,
[credits]
Cat GIF shown as a reminder: 'Cat Broken Cat GIF', Tenor, https://tenor.com/byRd2.gif
System Tray Application Icon: 'Drink free icon', by Freepik - Flaticon, https://www.flaticon.com/free-icon/drink_169965
"""

import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import schedule
import time
import threading
import pystray
from pystray import MenuItem, Icon
import os

# Path to the GIF and icon
gif_path = os.path.join(os.path.dirname(__file__), 'cat-broken-cat.gif')
icon_path = os.path.join(os.path.dirname(__file__), 'drink.ico')

# Function to create a window that displays the GIF
def show_gif():
    print("show_gif called")  # Debug statement
    win = Toplevel()
    win.title("Drink Water Reminder")

    # Set initial geometry (size and position)
    window_width = 300
    window_height = 300
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Load the GIF
    print(f"Loading GIF from: {gif_path}")

    img = Image.open(gif_path)

    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(img.copy()))
            img.seek(len(frames))  # Move to the next frame
    except EOFError:
        print(f"Loaded {len(frames)} frames.")

    lbl = tk.Label(win)
    lbl.pack()

    def update_frame(frame_idx):
        if frames:  # Check if frames list is not empty
            lbl.config(image=frames[frame_idx])
            frame_idx = (frame_idx + 1) % len(frames)
            win.after(100, update_frame, frame_idx)

    update_frame(0)

    # Create a close button
    close_button = tk.Button(win, text="Close", command=win.destroy)
    close_button.pack(pady=10)  # Add some padding for aesthetics

    win.attributes("-topmost", True)
    win.after(10000, win.destroy)  # Automatically close after 10 seconds

    # Show the window
    win.deiconify()  # Make the window visible


# Schedule the GIF reminders
def setup_schedule():
    schedule.every(15).seconds.do(show_gif)

    print("Scheduler started.")  # Debug statement

    while True:
        print("Checking schedule...")  # Debug statement
        schedule.run_pending()
        time.sleep(1)


# Function to quit the application
def quit_app(icon, item):
    icon.stop()
    root.quit()


# Create the system tray icon
def create_tray_icon():
    icon = Icon("drink_reminder", Image.open(icon_path), "Drink Reminder", menu=pystray.Menu(
        MenuItem("Quit", quit_app)
    ))
    icon.run()


# Run the scheduling in the background
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Start the scheduling in a separate thread
    schedule_thread = threading.Thread(target=setup_schedule, daemon=True)
    schedule_thread.start()

    # Create and run the system tray icon
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()

    root.mainloop()
