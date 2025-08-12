const express = require('express');
const path = require('path');
const axios = require('axios');
const multer = require('multer');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'frontend/build')));

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF files are allowed'), false);
    }
  },
});

// API Configuration
const API_BASE_URL = 'https://r8d6id8ewc.execute-api.eu-west-2.amazonaws.com/prod';

// Health check endpoint
app.get('/api/health', async (req, res) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      message: 'Health check failed',
      error: error.message 
    });
  }
});

// Upload letter endpoint
app.post('/api/upload-letter', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ 
        status: 'error', 
        message: 'No file uploaded' 
      });
    }

    // Convert file to base64
    const fileBuffer = req.file.buffer;
    const base64Data = fileBuffer.toString('base64');

    // Prepare request body for Lambda
    const requestBody = {
      file_data: base64Data,
      filename: req.file.originalname
    };

    // Call AWS Lambda function
    const response = await axios.post(`${API_BASE_URL}/upload-letter`, requestBody, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 second timeout
    });

    res.json(response.data);
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ 
      status: 'error', 
      message: 'Failed to process PDF',
      error: error.message 
    });
  }
});

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/build', 'index.html'));
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error('Server error:', error);
  res.status(500).json({ 
    status: 'error', 
    message: 'Internal server error',
    error: error.message 
  });
});

app.listen(PORT, () => {
  console.log(`🚀 AI Locus Agent server running on port ${PORT}`);
  console.log(`📱 Frontend: http://localhost:${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
});
