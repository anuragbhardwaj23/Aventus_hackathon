const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// Serve the HTML page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Handle the image upload and saving
app.post('/upload', (req, res) => {
  let data = '';
  
  req.on('data', chunk => {
    data += chunk;
  });
  
  req.on('end', () => {
    // Parse the image data from the request
    const imageData = JSON.parse(data);
    const dataURL = imageData.dataURL;
    const name = imageData.name;
    const ticketId = imageData.ticketId;
    
    // Directory where you want to save the image
    const saveDirectory = path.join(__dirname, 'images');
    
    // Create the directory if it doesn't exist
    if (!fs.existsSync(saveDirectory)) {
      fs.mkdirSync(saveDirectory);
    }
    
    // Generate a filename based on the name and ticket ID
    const filename = `${name}_${ticketId}.png`;
    const filePath = path.join(saveDirectory, filename);
    
    // Extract the base64 data from the data URL
    const base64Data = dataURL.replace(/^data:image\/png;base64,/, '');
    
    // Write the image file
    fs.writeFile(filePath, base64Data, 'base64', (error) => {
      if (error) {
        console.error('Failed to save the image:', error);
        res.status(500).send('Failed to save the image');
      } else {
        console.log('Image saved successfully:', filePath);
        res.send('Image saved successfully');
      }
    });
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});