import uuid
import easyocr
import numpy as np
import cv2

from typing import Callable, Optional, Union
from e2b import Sandbox as SandboxBase


class Sandbox(SandboxBase):
    default_template = "desktop"

    def screenshot(
        self,
        name: str,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None,
    ):
        """
        Take a screenshot and save it to the given name.
        :param name: The name of the screenshot file to save locally.
        """
        screenshot_path = f"/home/user/screenshot-{uuid.uuid4()}.png"

        self.commands.run(
            f"scrot --pointer {screenshot_path}",
            on_stderr=on_stderr,
            on_stdout=on_stdout,
            cwd="/home/user",
        )

        with open(name, "wb") as f:
            file = self.files.read(screenshot_path, format="bytes")
            f.write(file)

    def left_click(self):
        """
        Left click on the current mouse position.
        """
        return self.pyautogui("pyautogui.click()")

    def double_click(self):
        """
        Double left click on the current mouse position.
        """
        return self.pyautogui("pyautogui.doubleClick()")

    def right_click(self):
        """
        Right click on the current mouse position.
        """
        return self.pyautogui("pyautogui.rightClick()")

    def middle_click(self):
        return self.pyautogui("pyautogui.middleClick()")

    def scroll(self, amount: int):
        return self.pyautogui(f"pyautogui.scroll({amount})")

    def mouse_move(
        self,
        x_or_coords: Union[int, tuple[int, int]],
        y: Optional[int] = None,
    ):
        """
        Move the mouse to the given coordinates.
        :param x_or_coords: The x coordinate or a tuple of (x, y).
        :param y: The y coordinate, if x_or_coords is not a tuple.
        """
        if isinstance(x_or_coords, tuple):
            x, y = x_or_coords
        return self.pyautogui(f"pyautogui.moveTo({x}, {y})")

    def locate_on_screen(self, text: str):
        """
        Locate the text on the screen and return the position.
        :param text: The text to locate.
        """

        # Take a screenshot
        screenshot_path = f"/home/user/screenshot-{uuid.uuid4()}.png"
        self.commands.run(f"scrot --pointer {screenshot_path}")
        image_bytes = self.files.read(screenshot_path, format="bytes")

        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Initialize EasyOCR reader
        reader = easyocr.Reader(["en"])

        # Perform OCR
        results = reader.readtext(image)

        # Find the text in the results
        for bbox, detected_text, prob in results:
            if text.lower() in detected_text.lower():
                # Calculate center of bounding box
                (top_left, top_right, bottom_right, bottom_left) = bbox
                center_x = (top_left[0] + bottom_right[0]) / 2
                center_y = (top_left[1] + bottom_right[1]) / 2
                return center_x, center_y
        return None

    def get_cursor_position(self):
        """
        Get the current cursor position.
        :return: A tuple with the x and y coordinates.
        """
        # We save the value to a file because stdout contains warnings about Xauthority.
        self.pyautogui(
            """
x, y = pyautogui.position()
with open("/tmp/cursor_position.txt", "w") as f:
    f.write(str(x) + " " + str(y))
"""
        )
        # pos is like this: 100 200
        pos = self.files.read("/tmp/cursor_position.txt")
        return tuple(map(int, pos.split(" ")))

    def get_screen_size(self):
        """
        Get the current screen size.
        :return: A tuple with the width and height.
        """
        # We save the value to a file because stdout contains warnings about Xauthority.
        self.pyautogui(
            """
width, height = pyautogui.size()
with open("/tmp/size.txt", "w") as f:
    f.write(str(width) + " " + str(height))
"""
        )
        # size is like this: 100 200
        size = self.files.read("/tmp/size.txt")
        return tuple(map(int, size.split(" ")))

    def write(self, text: str):
        """
        Write the given text at the current cursor position.
        :param text: The text to write.
        """
        return self.pyautogui(f"pyautogui.write({text!r})")

    def hotkey(self, *keys):
        """
        Press a hotkey.
        :param keys: The keys to press.
        """
        return self.pyautogui(f"pyautogui.hotkey({keys!r})")

    def open(self, file_or_url: str):
        """
        Open a file or a URL in the default application.
        :param file_or_url: The file or URL to open.
        """
        return self.commands.run(f"xdg-open {file_or_url}", background=True)

    def install_package(self, package: str):
        """
        Install a package with apt.
        :param package: The package to install.
        """
        return self.commands.run(f"apt-get install -y {package}")

    @staticmethod
    def _wrap_pyautogui_code(code: str):
        return f"""
import pyautogui
import os
import Xlib.display

display = Xlib.display.Display(os.environ["DISPLAY"])
pyautogui._pyautogui_x11._display = display

{code}
exit(0)
"""

    def pyautogui(
        self,
        pyautogui_code: str,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None,
    ):
        code_path = f"/home/user/code-{uuid.uuid4()}.py"

        code = self._wrap_pyautogui_code(pyautogui_code)

        self.files.write(code_path, code)

        out = self.commands.run(
            f"python {code_path}",
            on_stdout=on_stdout,
            on_stderr=on_stderr,
        )
        return out
