const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const axios = require('axios');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.GATEWAY_PORT || 3001;
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:5002';

// Trust proxy for rate limiting
app.set('trust proxy', 1);

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Logging
app.use(morgan('combined'));

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rate limiting (disabled for development)
// const limiter = rateLimit({
//   windowMs: 15 * 60 * 1000, // 15 minutes
//   max: 100, // limit each IP to 100 requests per windowMs
//   message: {
//     error: 'Too many requests from this IP, please try again later.',
//     status: 'error'
//   }
// });
// app.use('/api/', limiter);

// Health check endpoint
app.get('/api/v1/health', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_BACKEND_URL}/api/v1/health`);
    res.json({
      ...response.data,
      gateway: 'healthy',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(503).json({
      error: 'Backend service unavailable',
      status: 'error',
      gateway: 'healthy',
      backend: 'unhealthy',
      timestamp: new Date().toISOString()
    });
  }
});

// Proxy patient data processing
app.post('/api/v1/process-patient-data', async (req, res) => {
  try {
    console.log('Gateway received request:', req.body);
    
    const response = await axios.post(
      `${PYTHON_BACKEND_URL}/api/v1/process-patient-data`,
      req.body,
      {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 30000 // 30 second timeout
      }
    );
    
    console.log('Backend response:', response.data);
    
    res.json({
      ...response.data,
      gateway_processed: true,
      gateway_timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Gateway error details:', {
      message: error.message,
      code: error.code,
      response: error.response?.data,
      status: error.response?.status
    });
    
    if (error.response) {
      // Backend returned an error
      res.status(error.response.status).json({
        ...error.response.data,
        gateway_processed: true,
        gateway_timestamp: new Date().toISOString()
      });
    } else if (error.code === 'ECONNABORTED') {
      // Timeout
      res.status(408).json({
        error: 'Request timeout',
        status: 'error',
        message: 'Backend processing took too long',
        gateway_processed: true,
        gateway_timestamp: new Date().toISOString()
      });
    } else {
      // Network or other error
      res.status(503).json({
        error: 'Service unavailable',
        status: 'error',
        message: 'Backend service is currently unavailable',
        gateway_processed: true,
        gateway_timestamp: new Date().toISOString()
      });
    }
  }
});

// Status endpoint
app.get('/api/status', async (req, res) => {
  try {
    const backendResponse = await axios.get(`${PYTHON_BACKEND_URL}/api/v1/status`);
    res.json({
      gateway: {
        status: 'operational',
        version: '1.0.0',
        timestamp: new Date().toISOString()
      },
      backend: backendResponse.data
    });
  } catch (error) {
    res.json({
      gateway: {
        status: 'operational',
        version: '1.0.0',
        timestamp: new Date().toISOString()
      },
      backend: {
        status: 'unavailable',
        error: error.message
      }
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Gateway error:', err);
  res.status(500).json({
    error: 'Internal gateway error',
    status: 'error',
    message: 'An unexpected error occurred',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    status: 'error',
    message: 'The requested endpoint does not exist',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`🚀 AI Locus Agent Gateway running on port ${PORT}`);
  console.log(`📡 Proxying to Python backend: ${PYTHON_BACKEND_URL}`);
  console.log(`🌐 Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
});
