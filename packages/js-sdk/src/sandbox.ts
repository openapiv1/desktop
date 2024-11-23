import { Sandbox as SandboxBase, SandboxOpts as SandboxOptsBase, ConnectionConfig } from 'e2b'
import { generateRandomId } from './utils'
// import { extractText } from './ocr'

export interface SandboxOpts extends SandboxOptsBase {
  livestream?: boolean
  onLivestreamStart?: (url: string) => void
}

export class Sandbox extends SandboxBase {
  protected static override readonly defaultTemplate: string = 'desktop'
  private static readonly streamBaseUrl = 'https://e2b.dev'

  private static async startLivestream(sandbox: Sandbox, apiKey: string, sandboxId: string, onLivestreamStart?: (url: string) => void) {
    // First we get the stream key
    const response = await fetch(`${this.streamBaseUrl}/api/stream/sandbox`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      },
      body: JSON.stringify({ sandboxId })
    })

    if (!response.ok) {
      throw new Error(`Failed to start livestream: ${response.statusText}`)
    }

    const data = await response.json()
    const command = 'ffmpeg -video_size 1024x768 -f x11grab -i :99 -c:v libx264 -c:a aac -g 50 -b:v 4000k -maxrate 4000k -bufsize 8000k -f flv rtmp://global-live.mux.com:5222/app/$STREAM_KEY'
    await sandbox.commands.run(command, {
      background: true,
      envs: {
        STREAM_KEY: data.streamKey
      },
    })
    const url = await sandbox.getLivestreamUrl()
    onLivestreamStart?.(url)
  }

  /**
   * Create a new sandbox from the default `desktop` sandbox template.
   *
   * @param opts connection options.
   *
   * @returns sandbox instance for the new sandbox.
   *
   * @example
   * ```ts
   * const sandbox = await Sandbox.create()
   * ```
   * @constructs Sandbox
   */
  static async create<S extends typeof Sandbox>(
    this: S,
    opts?: SandboxOpts
  ): Promise<InstanceType<S>>
  /**
   * Create a new sandbox from the specified sandbox template.
   *
   * @param template sandbox template name or ID.
   * @param opts connection options.
   *
   * @returns sandbox instance for the new sandbox.
   *
   * @example
   * ```ts
   * const sandbox = await Sandbox.create('<template-name-or-id>')
   * ```
   * @constructs Sandbox
   */
  static async create<S extends typeof Sandbox>(
    this: S,
    template: string,
    opts?: SandboxOpts
  ): Promise<InstanceType<S>>
  static async create<S extends typeof Sandbox>(
    this: S,
    templateOrOpts?: SandboxOpts | string,
    opts?: SandboxOpts
  ): Promise<InstanceType<S>> {
    const { template, sandboxOpts } =
      typeof templateOrOpts === 'string'
        ? { template: templateOrOpts, sandboxOpts: opts }
        : { template: this.defaultTemplate, sandboxOpts: templateOrOpts }

    const config = new ConnectionConfig(sandboxOpts)

    const sandboxId = config.debug
      ? 'debug_sandbox_id'
      : await this.createSandbox(
        template,
        sandboxOpts?.timeoutMs ?? this.defaultSandboxTimeoutMs,
        sandboxOpts
      )

    const sbx = new this({ sandboxId, ...config }) as InstanceType<S>

    if (sandboxOpts?.livestream) {
      this.startLivestream(sbx, config.apiKey!, sandboxId, sandboxOpts?.onLivestreamStart)
    }

    return sbx
  }

  async getLivestreamUrl() {
    return `${Sandbox.streamBaseUrl}/stream/sandbox/${this.sandboxId}`
  }

  /**
   * Take a screenshot and save it to the given name.
   * @param format - The format of the screenshot.
   * @returns A Uint8Array bytes representation of the screenshot.
   */
  async takeScreenshot(): Promise<Uint8Array>
  /**
   * Take a screenshot and save it to the given name.
   * @param format - The format of the screenshot.
   * @returns A Uint8Array bytes representation of the screenshot.
   */
  async takeScreenshot(format: 'bytes'): Promise<Uint8Array>
  /**
   * Take a screenshot and save it to the given name.
   * @returns A Blob representation of the screenshot.
   */
  async takeScreenshot(format: 'blob'): Promise<Blob>
  /**
   * Take a screenshot and save it to the given name.
   * @returns A ReadableStream of bytes representation of the screenshot.
   */
  async takeScreenshot(format: 'stream'): Promise<ReadableStream<Uint8Array>>
  async takeScreenshot(format: 'bytes' | 'blob' | 'stream' = 'bytes') {
    const path = `/home/user/screenshot-${generateRandomId()}.png`
    await this.commands.run(`scrot --pointer ${path}`)

    // @ts-expect-error
    const file = await this.files.read(path, { format })
    return file
  }

  /**
   * Left click on the current mouse position.
   */
  async leftClick() {
    return this.runPyautoguiCode('pyautogui.click()')
  }

  /**
   * Double left click on the current mouse position.
   */
  async doubleClick() {
    return this.runPyautoguiCode('pyautogui.click(clicks=2, interval=0.25)')
  }

  /**
   * Right click on the current mouse position.
   */
  async rightClick() {
    return this.runPyautoguiCode('pyautogui.rightClick()')
  }

  /**
   * Middle click on the current mouse position.
   */
  async middleClick() {
    return this.runPyautoguiCode('pyautogui.middleClick()')
  }

  /**
   * Scroll the mouse wheel by the given amount.
   * @param amount - The amount to scroll.
   */
  async scroll(amount: number) {
    return this.runPyautoguiCode(`pyautogui.scroll(${amount})`)
  }

  /**
   * Write the given text at the current cursor position.
   * @param text - The text to write.
   */
  async write(text: string) {
    return this.runPyautoguiCode(`pyautogui.write(${JSON.stringify(text)})`)
  }

  /**
   * Press a key.
   * @param key - The key to press (e.g. "enter", "space", "backspace", etc.).
   */
  async press(key: string) {
    return this.runPyautoguiCode(`pyautogui.press(${JSON.stringify(key)})`)
  }

  /**
   * Press a hotkey.
   * @param keys - The keys to press (e.g. `hotkey("ctrl", "c")` will press Ctrl+C).
   */
  async hotkey(...keys: string[]) {
    const keysString = keys.map(key => JSON.stringify(key)).join(', ')
    return this.runPyautoguiCode(`pyautogui.hotkey(${keysString})`)
  }

  /**
   * Open a file or a URL in the default application.
   * Note that you'll need to wait for the application to be opened.
   * @param fileOrUrl - The file or URL to open.
   */
  async open(fileOrUrl: string) {
    return this.commands.run(`xdg-open ${fileOrUrl}`, { background: true })
  }

  /**
   * Move the mouse to the given coordinates.
   * @param x - The x coordinate.
   * @param y - The y coordinate.
   */
  async moveMouse(x: number, y: number) {
    return this.runPyautoguiCode(`pyautogui.moveTo(${x}, ${y})`)
  }

  /**
   * Get the current mouse position.
   * @returns An object with `x` and `y` coordinates.
   */
  async getCursorPosition() {
    // We save the value to a file because stdout contains warnings about Xauthority.
    await this.runPyautoguiCode(`
x, y = pyautogui.position()
with open("/tmp/cursor_position.txt", "w") as f:
    f.write(str(x) + " " + str(y))
`)
    // pos is like this: 100 200
    const pos = await this.files.read('/tmp/cursor_position.txt')
    const [x, y] = pos.split(' ').map(Number)
    return { x, y }
  }

  /**
   * Get the current screen size.
   * @returns An object with `width` and `height` properties.
   */
  async getScreenSize() {
    // We save the value to a file because stdout contains warnings about Xauthority.
    await this.runPyautoguiCode(`
width, height = pyautogui.size()
with open("/tmp/size.txt", "w") as f:
    f.write(str(width) + " " + str(height))
`)
    // Size is like this: 100 200
    const size = await this.files.read('/tmp/size.txt')
    const [width, height] = size.split(' ').map(Number)
    return { width, height }
  }

  // /**
  //  * Locate the given text on the screen.
  //  * @param text - The text to locate.
  //  * @returns An object with the following properties:
  //  * - `x0`: The left coordinate of the text.
  //  * - `y0`: The top coordinate of the text.
  //  * - `x1`: The right coordinate of the text.
  //  * - `y1`: The bottom coordinate of the text.
  //  * - `xCenter`: The center x coordinate of the text.
  //  * - `yCenter`: The center y coordinate of the text.
  //  */
  // async locateTextOnScreen(text: string) {
  //   const imageData = await this.takeScreenshot()
  //   const textPositions = await extractText(imageData)
  //   const textPosition = textPositions.find((t) => t.text.includes(text))
  //   if (!textPosition) return null
  //   return {
  //     x0: textPosition.bbox.x0, // left
  //     y0: textPosition.bbox.y0, // top
  //     x1: textPosition.bbox.x1, // right
  //     y1: textPosition.bbox.y1, // bottom
  //     xCenter: (textPosition.bbox.x0 + textPosition.bbox.x1) / 2,
  //     yCenter: (textPosition.bbox.y0 + textPosition.bbox.y1) / 2,
  //   }
  // }


  /**
   * Run the given Python code that uses pyautogui.
   */
  async runPyautoguiCode(
    code: string,
    opts: {
      onStdout?: (data: string) => void
      onStderr?: (data: string) => void
    } = {},
  ) {
    const path = `/home/user/code-${generateRandomId()}.py`
    const wrappedCode = this.wrapPyautoguiCode(code)
    await this.files.write(path, wrappedCode)
    const out = await this.commands.run(`python ${path}`, {
      onStdout: opts.onStdout,
      onStderr: opts.onStderr,
    })
    return out
  }

  private wrapPyautoguiCode(code: string) {
    return `
import pyautogui
import os
import Xlib.display

display = Xlib.display.Display(os.environ["DISPLAY"])
pyautogui._pyautogui_x11._display = display

${code}
exit(0)
`
  }
}
