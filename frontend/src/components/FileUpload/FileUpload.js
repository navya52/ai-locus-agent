import React from 'react';
import styled from 'styled-components';
import { colors, typography, spacing, borderRadius, shadows } from '../../styles/theme';

const InputSection = styled.div`
  margin-bottom: ${spacing.xl};
`;

const InputLabel = styled.label`
  display: block;
  margin-bottom: ${spacing.md};
  font-weight: ${typography.fontWeight.semibold};
  color: ${colors.text};
  font-size: ${typography.fontSize.md};
`;

const FileUploadArea = styled.div`
  border: 2px dashed ${colors.border};
  border-radius: ${borderRadius.lg};
  padding: ${spacing.xl};
  text-align: center;
  background: ${colors.surfaceLight};
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;

  &:hover {
    border-color: ${colors.primary};
    background: ${colors.background};
  }

  &.has-file {
    border-color: ${colors.success};
    background: ${colors.background};
  }
`;

const FileInput = styled.input`
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
`;

const UploadIcon = styled.div`
  font-size: 48px;
  margin-bottom: ${spacing.md};
  color: ${colors.primary};
`;

const UploadText = styled.div`
  font-size: ${typography.fontSize.lg};
  font-weight: ${typography.fontWeight.medium};
  color: ${colors.text};
  margin-bottom: ${spacing.sm};
`;

const UploadSubtext = styled.div`
  font-size: ${typography.fontSize.sm};
  color: ${colors.textLight};
`;

const SelectedFile = styled.div`
  background: ${colors.success};
  color: white;
  padding: ${spacing.md};
  border-radius: ${borderRadius.md};
  margin-top: ${spacing.md};
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: ${typography.fontSize.sm};
  font-weight: ${typography.fontWeight.medium};
`;

const RemoveFileButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 4px 8px;
  border-radius: ${borderRadius.sm};
  cursor: pointer;
  font-size: ${typography.fontSize.xs};
  transition: background 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }
`;

const SubmitButton = styled.button`
  background: ${colors.primary};
  color: white;
  border: none;
  padding: ${spacing.md} ${spacing.xl};
  border-radius: ${borderRadius.md};
  font-size: ${typography.fontSize.md};
  font-weight: ${typography.fontWeight.semibold};
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  margin-top: ${spacing.md};

  &:hover:not(:disabled) {
    background: ${colors.secondary};
    transform: translateY(-1px);
    box-shadow: ${shadows.md};
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    background: ${colors.textLight};
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const FileUpload = ({ 
  selectedFile, 
  onFileSelect, 
  onRemoveFile, 
  onUpload, 
  loading, 
  error 
}) => {
  const handleClick = () => {
    document.getElementById('file-input').click();
  };

  return (
    <InputSection>
      <InputLabel htmlFor="file-input">
        Upload Clinical Letter (PDF)
      </InputLabel>
      
      <FileUploadArea 
        onClick={handleClick}
        className={selectedFile ? 'has-file' : ''}
      >
        <FileInput
          id="file-input"
          type="file"
          accept=".pdf"
          onChange={onFileSelect}
        />
        
        {!selectedFile ? (
          <>
            <UploadIcon>📄</UploadIcon>
            <UploadText>Click to select PDF file</UploadText>
            <UploadSubtext>
              Drag and drop or click to browse
            </UploadSubtext>
          </>
        ) : (
          <SelectedFile>
            <span>📄 {selectedFile.name}</span>
            <RemoveFileButton onClick={(e) => {
              e.stopPropagation();
              onRemoveFile();
            }}>
              Remove
            </RemoveFileButton>
          </SelectedFile>
        )}
      </FileUploadArea>

      {error && (
        <div style={{ 
          color: colors.danger, 
          marginTop: spacing.sm,
          fontSize: typography.fontSize.sm 
        }}>
          {error}
        </div>
      )}

      <SubmitButton 
        onClick={onUpload} 
        disabled={!selectedFile || loading}
      >
        {loading ? 'Processing...' : 'Process Letter'}
      </SubmitButton>
    </InputSection>
  );
};

export default FileUpload;
