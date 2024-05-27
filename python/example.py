import logging

from dotenv import load_dotenv
from e2b_desktop import Desktop

load_dotenv()

logging.basicConfig(level=logging.INFO)

with Desktop() as desktop:
    desktop.pyautogui(
        """
pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.
"""
    )

    desktop.screenshot("screenshot.png")
