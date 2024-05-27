import logging
import time

from dotenv import load_dotenv
from e2b_desktop import Desktop

load_dotenv()

logging.basicConfig(level=logging.INFO)

with Desktop() as desktop:
    desktop.screenshot("screenshot-1.png")

    # Create file and open text editor
    file = "/home/user/test.txt"
    desktop.filesystem.write(file, "world!")
    desktop.start_command(f"mousepad {file}")
    time.sleep(2)  # The mousepad command does not exit until you close the window
    desktop.screenshot("screenshot-2.png")

    # Write "Hello, world!"
    desktop.pyautogui(
        """
pyautogui.write("Hello, ")
"""
    )
    desktop.screenshot("screenshot-3.png")
