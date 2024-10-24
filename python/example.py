import time

from dotenv import load_dotenv
from e2b_desktop import Sandbox

load_dotenv()

print("Starting desktop sandbox...")
desktop = Sandbox()
print("Desktop Sandbox started, ID:", desktop.sandbox_id)

desktop.screenshot("1.png")

print("Locating 'Applications' on screen...")
pos = desktop.locate_on_screen("Applications")
if pos is None:
    raise Exception("Not found on screen")

print("Moving mouse to 'Applications' and clicking...")
desktop.mouse_move(pos)
desktop.left_click()

time.sleep(1)
desktop.screenshot("2.png")
