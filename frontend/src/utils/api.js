import axios from 'axios';
import config from '../config';
import { API_ENDPOINTS } from '../constants';

const apiClient = axios.create({
  baseURL: config.apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadLetter = async (fileData, filename) => {
  try {
    const response = await apiClient.post(API_ENDPOINTS.UPLOAD_LETTER, {
      fileData,
      filename
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Upload failed');
  }
};

export const getLetters = async () => {
  try {
    const response = await apiClient.get(API_ENDPOINTS.GET_LETTERS);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to fetch letters');
  }
};

export const getFile = async (storageId) => {
  try {
    const response = await apiClient.get(`${API_ENDPOINTS.GET_FILE}?storage_id=${storageId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to get file');
  }
};

export const downloadFile = async (storageId, filename) => {
  try {
    const fileData = await getFile(storageId);
    const link = document.createElement('a');
    link.href = fileData.data.download_url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    throw new Error('Download failed');
  }
};
