import { useState, useCallback } from 'react';
import { uploadLetter } from '../utils/api';
import { FILE_TYPES, MAX_FILE_SIZE } from '../constants';

export const useFileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const validateFile = useCallback((file) => {
    if (!file) {
      throw new Error('Please select a file');
    }

    if (file.type !== FILE_TYPES.PDF) {
      throw new Error('Only PDF files are supported');
    }

    if (file.size > MAX_FILE_SIZE) {
      throw new Error('File size must be less than 10MB');
    }

    return true;
  }, []);

  const handleFileSelect = useCallback((event) => {
    const file = event.target.files[0];
    setError(null);
    
    try {
      validateFile(file);
      setSelectedFile(file);
    } catch (err) {
      setError(err.message);
      setSelectedFile(null);
    }
  }, [validateFile]);

  const removeFile = useCallback(() => {
    setSelectedFile(null);
    setError(null);
  }, []);

  const uploadFile = useCallback(async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const reader = new FileReader();
      
      reader.onload = async (e) => {
        try {
          const base64Data = e.target.result.split(',')[1];
          const response = await uploadLetter(base64Data, selectedFile.name);
          setResults(response);
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };

      reader.onerror = () => {
        setError('Failed to read file');
        setLoading(false);
      };

      reader.readAsDataURL(selectedFile);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }, [selectedFile]);

  return {
    selectedFile,
    loading,
    error,
    results,
    handleFileSelect,
    removeFile,
    uploadFile
  };
};
