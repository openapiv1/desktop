import logging
import time

from dotenv import load_dotenv
from e2b_desktop import Desktop

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

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

# === OPENING FILE ===
# Create file inside the sandbox and open it in a text editor
text_file_path = "/home/user/test.txt"
# `data` can be a string or bytes
desktop.files.write(text_file_path, "Hello, world!")
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


start_time = time.time()
desktop.kill()
end_time = time.time()
print(f"desktop.kill() took {end_time - start_time} seconds")

# with Desktop() as desktop: # Using the `with` clause, the sandbox automatically calls `close()` on itself once we run all the code inside the clause.
#     desktop.screenshot("screenshot-1.png")

#     # Create file and open text editor
#     file = "/home/user/test.txt"
#     desktop.filesystem.write(file, "world!")

#     # Normally, we would use `desktop.process.start_and_wait()` to run a new process
#     # and wait until it finishes.
#     # However, the mousepad command does not exit until you close the window so we
#     # we need to just start the process and run it in the background so it doesn't
#     # block our code.
#     desktop.process.start(
#         f"mousepad {file}",
#         env_vars={"DISPLAY": desktop.DISPLAY},
#         on_stderr=lambda stderr: print(stderr),
#         on_stdout=lambda stdout: print(stdout),
#         cwd="/home/user",
#     )
#     time.sleep(2)
#     #####

#     desktop.screenshot("screenshot-2.png")

#     # Write "Hello, " in the text editor
#     desktop.pyautogui(
#         """
# pyautogui.write("Hello, ")
# """
#     )
#     desktop.screenshot("screenshot-3.png")
