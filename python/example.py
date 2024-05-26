from e2b import Sandbox
from dotenv import load_dotenv

load_dotenv()


code = """
import pyautogui
import os
from pyvirtualdisplay.display import Display
import Xlib.display

disp = Display(visible=True, size=(1024, 768), backend="xvfb", use_xauth=True)
disp.start()

pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])

pyautogui.move(400, 0)

pyautogui.screenshot('screenshot.png')
disp.stop()
"""

with Sandbox(template="desktop") as sandbox:
    # Manipulate desktop
    sandbox.filesystem.write("/home/user/code.py", code)
    result = sandbox.process.start_and_wait(
        "python /home/user/code.py",
        env_vars={"DISPLAY": ":1"},
    )
    print(result.stderr)

    # Get screenshot
    screenshot_path = "/home/user/screenshot.png"
    # result = sandbox.process.start_and_wait(
    #     f"xfce4-screenshooter -f -s {screenshot_path}",
    #     env_vars={"DISPLAY": ":1"},
    # )
    # print(result.stdout)

    ls = sandbox.filesystem.list("/home/user")
    print(ls)

    file = sandbox.download_file(screenshot_path)
    with open("screenshot.png", "wb") as f:
        f.write(file)
