// API Configuration
const config = {
  // Local server endpoint (will be replaced with EC2 IP)
  API_BASE_URL: process.env.NODE_ENV === 'production' 
    ? 'https://ov02sq5ll7.execute-api.eu-west-2.amazonaws.com/Prod' 
    : 'http://localhost:3000',
  
  // API endpoints
  UPLOAD_ENDPOINT: '/upload-letter',
  GET_LETTERS_ENDPOINT: '/get-letters',
  GET_FILE_ENDPOINT: '/get-file',
  HEALTH_ENDPOINT: '/health',
  
  // Full API URLs
  getUploadUrl: () => `${config.API_BASE_URL}${config.UPLOAD_ENDPOINT}`,
  getLettersUrl: () => `${config.API_BASE_URL}${config.GET_LETTERS_ENDPOINT}`,
  getFileUrl: () => `${config.API_BASE_URL}${config.GET_FILE_ENDPOINT}`,
  getHealthUrl: () => `${config.API_BASE_URL}${config.HEALTH_ENDPOINT}`,
};

export default config;
