# E2B Desktop Environment

This repo shows how to run [E2B's sandboxes](https://e2b.dev/docs/sandbox/overview) with a graphical desktop-like environment. We built this using our [custom sandboxes](https://e2b.dev/docs/sandbox/templates/overview) feature (all the files and code used for this custom sandbox are in the [`template/`](https://github.com/e2b-dev/desktop/tree/main/template) folder.
The desktop-like environment allows you to start applications like file explorers, browsers, terminals, notes, etc.

You can use PyAutoGUI to control the environment programmatically.

The desktop-like environment is based on Linux and [Xfce](https://www.xfce.org/) at the moment. We chose Xfce because it's a fast and lightweight environment that's also popular and actively supported. Let us know if you need something else or if Xfce doesn't work for you.

## Example

The [example script](python/example.py) in this repo does the following and takes a screenshot after each action:

**1. Start the sandbox with a desktop environment**

Spawn a new sandbox and take a screenshot.

```python
with Desktop(timeout=60) as desktop:
    desktop.screenshot("screenshot.png")
```


![Step 1](python/screenshot-1.png)

---

**2. Open the text editor**

Create a new file, write to the file, and open the file using Xfce's text editor called [Mousepad](https://docs.xfce.org/apps/mousepad/start).

```python
with Desktop(timeout=60) as desktop:
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
```

![Step 2](python/screenshot-2.png)

---

**3. Use PyAutoGUI**

Use PyAutoGUI to write new text in the text editor.

```python
with Desktop(timeout=60) as desktop:
  pyautogui_code = """
    pyautogui.write("Hello, ")
  """
  desktop.pyautogui(pyaytogui_code)
```

![Step 3](python/screenshot-3.png)

## Caveats

#### Use `desktop_sandbox.screenshot()` instead of `pyautogui.screenshot()`
The official PythonAutoGUI's screenshot method doesn't capture the mouse pointer. If you want to take a screenshot with the mouse pointer, use our implementation.
```py
from e2b_desktop import Desktop
with Desktop() as desktop:
    desktop.screenshot("screenshot-name.png")
```

## How to run the example

**1. Install dependencies**

```bash
cd python && poetry install
```

**2. Add your `E2B_API_KEY=` to the `python/.env` file**
Get your E2B API key [here](https://e2b.dev/docs/getting-started/api-key).

Visit [E2B's docs](https://e2b.dev/docs/getting-started/api-key) to get your API key.

**3. (Optional) Modify the script**

Modify the [`python/example.py`](python/example.py) file to do what you want — for example, to move the mouse to the coordinates (100, 150), you can add the following line to the `desktop.pyautogui(<code>)` call:

```python
pyautogui.moveTo(100, 150)
```

> Running `desktop.pyautogui(<code>)` multiple times is fine.

> You can use all the methods from the [E2B SDK](https://e2b.dev/docs/sandbox/overview) to interact with the desktop.

**4. Run the script**

```bash
poetry run python example.py
```

**5. Inspect the screenshots**

After the script is finished, inspect the screenshots by checking them in the `python/` directory.

**6. (Optional) Modify the template**

If you want to preinstall dependencies you can modify the desktop template by editing the `template/*` files and then creating a [custom template](https://e2b.dev/docs/guide/custom-sandbox).

To spawn your custom sandbox, you need to pass the template name or ID to the constructor
```python
from e2b_desktop import Desktop

template_name_or_id = "my-sandbox-template"
with Desktop(template_name_or_id) as desktop:
  # ... perform actions in the sandbox
```
