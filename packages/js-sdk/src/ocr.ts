// import Tesseract from 'tesseract.js'

// export async function extractText(imageData: Uint8Array) {
//   try {
//     // Convert Uint8Array to a base64 string
//     const result = await Tesseract.recognize(
//       imageData,
//       'eng'
//     );

//     // Get all words first
//     const words = result.data.words;
//     const lines: typeof words[] = [];
//     let currentLine: typeof words = [];

//     // Sort words by y-coordinate (top to bottom)
//     words.sort((a, b) => a.bbox.y0 - b.bbox.y0);

//     // Process each word
//     words.forEach((word, i) => {
//       if (currentLine.length === 0) {
//         currentLine.push(word);
//       } else {
//         const lastWord = currentLine[currentLine.length - 1];

//         // Check if words are on roughly the same line (allowing for small variations)
//         const verticalOverlap = Math.abs(word.bbox.y0 - lastWord.bbox.y0) < 15;

//         // Calculate horizontal gap between words
//         const horizontalGap = word.bbox.x0 - lastWord.bbox.x1;
//         // Use average word width to determine if gap is too large
//         const avgWordWidth = (word.bbox.x1 - word.bbox.x0 + lastWord.bbox.x1 - lastWord.bbox.x0) / 2;
//         console.log({ avgWordWidth, horizontalGap })
//         const isCloseEnough = horizontalGap < avgWordWidth * 2; // Adjust multiplier as needed

//         if (verticalOverlap && isCloseEnough) {
//           currentLine.push(word);
//         } else {
//           // Start new line
//           if (currentLine.length > 0) {
//             lines.push([...currentLine]);
//           }
//           currentLine = [word];
//         }
//       }
//     });

//     // Add the last line if it exists
//     if (currentLine.length > 0) {
//       lines.push(currentLine);
//     }

//     // Convert lines to sentences with bounding boxes
//     const sentences = lines.map(line => {
//       const text = line.map(word => word.text).join(' ').trim();

//       const bbox = {
//         x0: Math.min(...line.map(w => w.bbox.x0)),
//         y0: Math.min(...line.map(w => w.bbox.y0)),
//         x1: Math.max(...line.map(w => w.bbox.x1)),
//         y1: Math.max(...line.map(w => w.bbox.y1))
//       };

//       const confidence = line.reduce((sum, word) => sum + word.confidence, 0) / line.length;

//       return {
//         text,
//         confidence,
//         bbox
//       };
//     });

//     sentences.forEach(sentence => {
//       console.log({
//         text: sentence.text,
//         confidence: sentence.confidence,
//         bbox: sentence.bbox
//       });
//     });

//     return sentences;
//   } catch (error) {
//     console.error('Error extracting text from image:', error);
//     throw error;
//   }
// }
