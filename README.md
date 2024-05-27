# E2B Desktop Environment

## How to use

1. Install dependencies

```bash
cd python && poetry install
```

2. Add your E2B API key to the `python/.env` file

3. (Optional) Modify the script

Modify the [`python/example.py`](python/example.py) file to do what you want — for example, to move the mouse to the coordinates (100, 150), you can add the following line to the `desktop.pyautogui(<code>)` call:

```python
pyautogui.moveTo(100, 150)
```

> Running `desktop.pyautogui(<code>)` multiple times is fine.

> You can use all the methods from E2B SDK to interact with the desktop too.

4. Run the script

```bash
poetry run python example.py
```

5. Inspect the screenshots

After the script has run, you can inspect the screenshots by checking them in the `python/` directory, where they were saved.

6. (Optional) Modify the template

If you want to preinstall dependencies you can modify the desktop template by editing the `template/*` files and then creating a custom template.

You will need to change the used template when creating the `Desktop`'s `template` argument in `python/example.py`.
