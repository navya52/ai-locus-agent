export const API_ENDPOINTS = {
  UPLOAD_LETTER: '/upload-letter',
  GET_LETTERS: '/get-letters',
  GET_FILE: '/get-file'
};

export const RISK_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high'
};

export const PHI_TYPES = {
  NAME: 'name',
  PHONE: 'phone',
  EMAIL: 'email',
  POSTCODE: 'postcode',
  ADDRESS: 'address',
  HOSPITAL_NUMBER: 'hospital_number',
  NHS_NUMBER: 'nhs_number'
};

export const PHI_TYPE_DESCRIPTIONS = {
  [PHI_TYPES.NAME]: 'Patient names (Mr./Mrs./Ms./Dr.)',
  [PHI_TYPES.PHONE]: 'Phone numbers',
  [PHI_TYPES.EMAIL]: 'Email addresses',
  [PHI_TYPES.POSTCODE]: 'UK postcodes',
  [PHI_TYPES.ADDRESS]: 'Street addresses',
  [PHI_TYPES.HOSPITAL_NUMBER]: 'Hospital/Patient ID numbers',
  [PHI_TYPES.NHS_NUMBER]: 'NHS numbers (kept for clinical use)'
};

export const FILE_TYPES = {
  PDF: 'application/pdf'
};

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
