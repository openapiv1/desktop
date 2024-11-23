import { config } from 'dotenv'
// import Tesseract from 'tesseract.js'
import { createCanvas, loadImage } from 'canvas'
import fs from 'fs'

import { Sandbox } from './dist'


config()

async function drawBoundingBoxes(imageData: Uint8Array, sentences: Array<{ bbox: any, text: string }>) {
  // Convert Uint8Array to a base64 string
  const base64Image = Buffer.from(imageData).toString('base64');
  const dataUrl = `data:image/png;base64,${base64Image}`;

  // Load the image
  const img = await loadImage(dataUrl);

  // Create canvas
  const canvas = createCanvas(img.width, img.height);
  const ctx = canvas.getContext('2d');

  // Draw the original image
  ctx.drawImage(img, 0, 0);

  // Style for the bounding boxes
  ctx.strokeStyle = 'red';
  ctx.lineWidth = 2;
  ctx.font = '16px Arial';
  ctx.fillStyle = 'red';

  // Draw boxes and labels for each sentence
  sentences.forEach((sentence, index) => {
    const { bbox } = sentence;
    const width = bbox.x1 - bbox.x0;
    const height = bbox.y1 - bbox.y0;

    // Draw rectangle
    ctx.strokeRect(bbox.x0, bbox.y0, width, height);

    // Draw text label above the box
    ctx.fillText(`${index + 1}: ${sentence.text}`, bbox.x0, bbox.y0 - 5);
  });

  // Save to file
  const outputPath = 'annotated_image.png';
  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync(outputPath, buffer);

  console.log(`Annotated image saved to: ${outputPath}`);
}

async function processImage(imageData: Uint8Array) {
  const sentences = await extractText(imageData)
  await drawBoundingBoxes(imageData, sentences);
}



// const sbx = await Sandbox.create()

// const vscodeSbx = await sbx
//   .files.makeDir('/home/user/project')
//   .open('code')
//   .wait(5000)
//   .fork('vscode')

// vscodeSbx.write('ai-generated-code')


const sbx = await Sandbox.create({
  livestream: true,
  onLivestreamStart: (url) => console.log('Livestream started', url)
})


// const command = "ffmpeg -video_size 1024x768 -f x11grab -i :99 -c:v libx264 -c:a aac  -g 50 -b:v 4000k -maxrate 4000k -bufsize 8000k -f flv rtmp://global-live.mux.com:5222/app/stream-key"
// const ffmpeg = await sbx.commands.run(command, { background: true, onStdout: (data) => console.log(data.toString()) })

// for (let i = 0; i < 30; i++) {
//   const x = Math.floor(Math.random() * 1024);
//   const y = Math.floor(Math.random() * 768);
//   await sbx.moveMouse(x, y);
//   await new Promise(resolve => setTimeout(resolve, 2000));
//   await sbx.rightClick();
//   console.log('right clicked', i)
// }


// await sbx.kill()


// await sbx.rightClick()
let imageData = await sbx.takeScreenshot()
await processImage(imageData)
// const pos = await sbx.locateTextOnScreen('Applications')
// if (!pos) throw new Error('Text not found on screen')
await sbx.moveMouse(384 + 150, 1024 - 80)
// await new Promise(resolve => setTimeout(resolve, 5000));
await sbx.doubleClick()
// await sbx.leftClick()
console.log('clicked')
await new Promise(resolve => setTimeout(resolve, 2000));
console.log('screenshot')
imageData = await sbx.takeScreenshot()
await processImage(imageData)
await sbx.kill()




// {
//   text: 'File System',
//   confidence: 95.43375396728516,
//   bbox: { x0: 33, y0: 228, x1: 107, y1: 241 }
// }
