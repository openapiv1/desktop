import time
import random

from dotenv import load_dotenv
from e2b_desktop import Sandbox

load_dotenv()

print("Starting desktop sandbox...")
desktop = Sandbox(livestream=True)
print("Desktop Sandbox started, ID:", desktop.sandbox_id)
livestream_url = desktop.get_livestream_url()
print("Livestream URL:", livestream_url)

desktop.take_screenshot("1.png")

print("Moving mouse to 'Applications' and clicking...")
desktop.move_mouse(100, 100)
desktop.left_click()

time.sleep(1)
desktop.take_screenshot("2.png")

for _ in range(20):
    x = random.randint(0, 1024)
    y = random.randint(0, 768)
    desktop.move_mouse(x, y)
    desktop.right_click()
    time.sleep(2)

desktop.kill()
