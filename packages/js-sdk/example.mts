import { config } from 'dotenv'
// import Tesseract from 'tesseract.js'
import { createCanvas, loadImage } from 'canvas'
import fs from 'fs'

config()
import { Sandbox } from './dist'



const sbx = await Sandbox.create({
  videoStream: true,
  onVideoStreamStart: (url) => console.log('Video stream started:', url)
})

// const command = "ffmpeg -video_size 1024x768 -f x11grab -i :99 -c:v libx264 -c:a aac  -g 50 -b:v 4000k -maxrate 4000k -bufsize 8000k -f flv rtmp://global-live.mux.com:5222/app/stream-key"
// const ffmpeg = await sbx.commands.run(command, { background: true, onStdout: (data) => console.log(data.toString()) })

for (let i = 0; i < 30; i++) {
  const x = Math.floor(Math.random() * 1024);
  const y = Math.floor(Math.random() * 768);
  await sbx.moveMouse(x, y);
  await new Promise(resolve => setTimeout(resolve, 2000));
  await sbx.rightClick();
  console.log('right clicked', i)
}


// await sbx.kill()


// // await sbx.rightClick()
// let imageData = await sbx.takeScreenshot()
// await processImage(imageData)
// // const pos = await sbx.locateTextOnScreen('Applications')
// // if (!pos) throw new Error('Text not found on screen')
// await sbx.moveMouse(384 + 150, 1024 - 80)
// // await new Promise(resolve => setTimeout(resolve, 5000));
// await sbx.doubleClick()
// // await sbx.leftClick()
// console.log('clicked')
// await new Promise(resolve => setTimeout(resolve, 2000));
// console.log('screenshot')
// imageData = await sbx.takeScreenshot()
// await processImage(imageData)
// await sbx.kill()




// {
//   text: 'File System',
//   confidence: 95.43375396728516,
//   bbox: { x0: 33, y0: 228, x1: 107, y1: 241 }
// }
