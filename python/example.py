import time

from dotenv import load_dotenv
from e2b_desktop import Sandbox

load_dotenv()

desktop = Sandbox()
print("Desktop Sandbox ID:", desktop.sandbox_id)

# desktop.screenshot("1.png")


pos = desktop.locate_on_screen("Applications")
if pos is None:
    raise Exception("Not found on screen")

desktop.mouse_move(pos)
desktop.left_click()

time.sleep(1)
desktop.screenshot("2.png")
