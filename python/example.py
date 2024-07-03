import logging
import time

from dotenv import load_dotenv
from e2b_desktop import Desktop

load_dotenv()

# Uncomment this to show debug logs in terminal
# Or if you want more detailed logs, you can pass `logging.DEBUG`
# logging.basicConfig(level=logging.INFO)

start_time = time.time()
desktop = Desktop(
    # Optional timeout after which the sandbox will be automatically killed.
    # If no timeout is specified, it fallbacks to the default timeout of 300 seconds.
    timeout=60,
)
end_time = time.time()
print(f"Desktop creation took {end_time - start_time} seconds")

# === TAKING SCREENSHOT ===
# This will take a screenshot of the desktop sandbox and save it to the current directory as `screenshot-1.png`.
desktop.screenshot("screenshot-1.png")
# ======================

# === OPENING FILE ===
# Create file inside the sandbox and open it in a text editor
text_file_path = "/home/user/test.txt"
# `data` can be a string or bytes
desktop.files.write(text_file_path, "world!")
# Open the text file in `mousepad` program.
# We need to run this command in background because `mousepad` will keep running until you close the window.
# Our code would get stuck here.
desktop.commands.run(
    f"mousepad {text_file_path}",
    background=True,
    envs={"DISPLAY": desktop.DISPLAY},
)
# Wait a bit to make sure it's really open.
time.sleep(2)
# Take a screenshot of the desktop with the open `mousepad` window.
desktop.screenshot("screenshot-2.png")
# ======================

# === USING PYAUTOGUI ===
# Write "Hello, " in the text editor
desktop.pyautogui("""
pyautogui.write("Hello, ")
""")
# Take a screenshot of the desktop with the text editor and "Hello, world" written.
desktop.screenshot("screenshot-3.png")
# ======================

start_time = time.time()
desktop.kill()
end_time = time.time()
print(f"desktop.kill() took {end_time - start_time} seconds")

# You can use the `with` clause to automatically kill the sandbox when you're done.
with Desktop(timeout=60) as desktop:
    desktop.screenshot("screenshot-4.png")
    # ...
