from e2b import Sandbox
from dotenv import load_dotenv
import uuid


load_dotenv()


class Desktop(Sandbox):
    DISPLAY = ":99"  # Must be the same as the start script env var

    def __init__(self):
        super().__init__(template="desktop")

    def screenshot(self, name: str):
        print("Getting screenshot")
        screenshot_path = "/home/user/screenshot.png"
        result = self.process.start_and_wait(
            f"import -window root {screenshot_path}",
            env_vars={"DISPLAY": self.DISPLAY},
        )
        print(result.stderr)

        print("Downloading screenshot")
        file = self.download_file(screenshot_path)
        with open(name, "wb") as f:
            f.write(file)

    @staticmethod
    def _wrap_pyautogui_code(code: str):
        return f"""
import pyautogui
import os
import Xlib.display

pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])

{code}

exit(0)
"""

    def control(self, pyautogui_code: str):
        code_path = f"/home/user/code-{uuid.uuid4()}.py"

        code = self._wrap_pyautogui_code(pyautogui_code)

        print("Writing code")
        self.filesystem.write(code_path, code)

        print("Running code")
        self.process.start_and_wait(
            f"python {code_path}",
            on_stdout=lambda stdout: print(stdout),
            on_stderr=lambda stderr: print(stderr),
            env_vars={"DISPLAY": self.DISPLAY},
        )


with Desktop() as desktop:
    desktop.control(
        """
currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.
print(currentMouseX, currentMouseY)

pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.
    """
    )

    desktop.screenshot("screenshot.png")
