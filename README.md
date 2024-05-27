# E2B Desktop Environment

## How to setup and modify

1. Install dependencies

```bash
cd python && poetry install
```

2. Add your E2B API key to the `python/.env` file

3. (Optional) Modify the script

Modify the `python/example.py` file to do what you want — for example, to move the mouse to the coordinates (100, 150), you can add the following line to the `desktop.pyautogui(<code>)` call:

```python
pyautogui.moveTo(100, 150)
```
> Running `desktop.pyautogui(<code>)` multiple times is fine.

4. Run the script

```bash
poetry run python example.py
```

5. Inspect the screenshot

After the script has run, you can inspect the screenshot by checking `python/screenshot.png`.

6. (Optional) Modify the template
You can modify the template by editing the `template/start-up.sh`, `template/e2b.Dockerfile` files and then creating a custom template. You will need to change the used template in when creating the sandbox in `python/example.py`.
