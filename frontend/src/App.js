import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { colors, typography, spacing } from './styles/theme';
import { getLetters, downloadFile } from './utils/api';
import { useFileUpload } from './hooks/useFileUpload';

// Components
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import ResultsTable from './components/ResultsTable';

// Styled Components
const AppContainer = styled.div`
  min-height: 100vh;
  background: ${colors.background};
  font-family: ${typography.fontFamily};
  color: ${colors.text};
  line-height: 1.6;
`;

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: ${spacing.xl} 24px;
`;

const Title = styled.h1`
  color: ${colors.text};
  font-size: ${typography.fontSize.xxl};
  font-weight: ${typography.fontWeight.bold};
  margin: 0 0 ${spacing.sm} 0;
  text-align: center;
`;

const Subtitle = styled.p`
  color: ${colors.textLight};
  font-size: ${typography.fontSize.md};
  text-align: center;
  margin: 0 0 ${spacing.xl} 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const TabContainer = styled.div`
  display: flex;
  margin-bottom: ${spacing.xl};
  border-bottom: 1px solid ${colors.border};
`;

const TabButton = styled.button`
  background: none;
  border: none;
  padding: ${spacing.md} ${spacing.lg};
  font-size: ${typography.fontSize.md};
  font-weight: ${typography.fontWeight.medium};
  color: ${colors.textLight};
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;

  &.active {
    color: ${colors.primary};
    border-bottom-color: ${colors.primary};
  }

  &:hover {
    color: ${colors.primary};
  }
`;

const LetterCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: ${spacing.lg};
  margin-bottom: ${spacing.md};
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid ${colors.border};
  transition: all 0.2s ease;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    transform: translateY(-1px);
  }
`;

const LetterHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${spacing.md};
  padding-bottom: ${spacing.md};
  border-bottom: 1px solid ${colors.border};
`;

const LetterTitle = styled.h3`
  margin: 0;
  color: ${colors.text};
  font-size: ${typography.fontSize.lg};
  font-weight: ${typography.fontWeight.semibold};
`;

const LetterDate = styled.span`
  color: ${colors.textLight};
  font-size: ${typography.fontSize.sm};
`;

const LetterDetails = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${spacing.md};
  margin-bottom: ${spacing.md};
`;

const LetterDetail = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${spacing.xs};
`;

const DetailLabel = styled.span`
  font-size: ${typography.fontSize.xs};
  font-weight: ${typography.fontWeight.semibold};
  color: ${colors.textLight};
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const DetailValue = styled.span`
  font-size: ${typography.fontSize.md};
  color: ${colors.text};
  font-weight: ${typography.fontWeight.medium};
`;

const LetterSummary = styled.div`
  margin-bottom: ${spacing.md};
`;

const SummaryText = styled.p`
  color: ${colors.text};
  line-height: 1.6;
  margin: 0;
`;

const LetterActions = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: ${spacing.md};
  border-top: 1px solid ${colors.border};
`;

const DownloadButton = styled.button`
  background: ${colors.primary};
  color: white;
  border: none;
  padding: ${spacing.sm} ${spacing.md};
  border-radius: 8px;
  font-size: ${typography.fontSize.sm};
  font-weight: ${typography.fontWeight.medium};
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: ${colors.secondary};
    transform: translateY(-1px);
  }
`;

const FileInfo = styled.div`
  display: flex;
  gap: ${spacing.md};
`;

const FileInfoText = styled.span`
  font-size: ${typography.fontSize.xs};
  color: ${colors.textLight};
`;

const ErrorMessage = styled.div`
  background: ${colors.danger};
  color: white;
  padding: ${spacing.md};
  border-radius: 8px;
  margin-bottom: ${spacing.md};
  font-size: ${typography.fontSize.sm};
`;

const LoadingState = styled.div`
  text-align: center;
  padding: ${spacing.xxl};
  color: ${colors.textLight};
`;

const Spinner = styled.div`
  border: 3px solid ${colors.border};
  border-top: 3px solid ${colors.primary};
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto ${spacing.md};

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [letters, setLetters] = useState([]);
  const [loadingLetters, setLoadingLetters] = useState(false);
  const [lettersError, setLettersError] = useState(null);

  const {
    selectedFile,
    loading: uploadLoading,
    error: uploadError,
    results,
    handleFileSelect,
    removeFile,
    uploadFile
  } = useFileUpload();

  useEffect(() => {
    if (activeTab === 'history') {
      fetchLetters();
    }
  }, [activeTab]);

  const fetchLetters = async () => {
    setLoadingLetters(true);
    setLettersError(null);
    
    try {
      const response = await getLetters();
      setLetters(response.letters || []);
    } catch (error) {
      setLettersError(error.message);
    } finally {
      setLoadingLetters(false);
    }
  };

  const handleDownload = async (storageId, filename) => {
    try {
      await downloadFile(storageId, filename);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  const getConfidencePercentage = (score) => {
    const numScore = score || 0;
    return numScore <= 1 ? Math.round(numScore * 100) : Math.round(numScore);
  };

  return (
    <AppContainer>
      <Header />
      
      <MainContent>
        <Title>AI Locus Agent</Title>
        <Subtitle>
          Upload clinical letters for AI-powered analysis, PHI detection, and risk assessment
        </Subtitle>

        <TabContainer>
          <TabButton 
            className={activeTab === 'upload' ? 'active' : ''}
            onClick={() => setActiveTab('upload')}
          >
            Upload Letter
          </TabButton>
          <TabButton 
            className={activeTab === 'history' ? 'active' : ''}
            onClick={() => setActiveTab('history')}
          >
            Processing History
          </TabButton>
        </TabContainer>

        {activeTab === 'upload' && (
          <>
            <FileUpload
              selectedFile={selectedFile}
              onFileSelect={handleFileSelect}
              onRemoveFile={removeFile}
              onUpload={uploadFile}
              loading={uploadLoading}
              error={uploadError}
            />

            {results && <ResultsTable results={results} />}
          </>
        )}

        {activeTab === 'history' && (
          <>
            {loadingLetters && (
              <LoadingState>
                <Spinner />
                Loading processing history...
              </LoadingState>
            )}

            {lettersError && (
              <ErrorMessage>
                Error loading letters: {lettersError}
              </ErrorMessage>
            )}

            {!loadingLetters && !lettersError && letters.length > 0 && (
              <div>
                {letters.map((letter) => (
                  <LetterCard key={letter.storage_id}>
                    <LetterHeader>
                      <LetterTitle>{letter.filename}</LetterTitle>
                      <LetterDate>
                        {new Date(letter.timestamp).toLocaleDateString('en-GB')}
                      </LetterDate>
                    </LetterHeader>

                    <LetterDetails>
                      <LetterDetail>
                        <DetailLabel>Word Count</DetailLabel>
                        <DetailValue>{letter.word_count}</DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>NHS Number</DetailLabel>
                        <DetailValue>{letter.nhs_number || 'Not found'}</DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>Risk Level</DetailLabel>
                        <DetailValue>
                          {letter.ai_summary?.risk_assessment?.overall_risk || 'Unknown'}
                        </DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>Confidence</DetailLabel>
                        <DetailValue>
                          {getConfidencePercentage(letter.ai_summary?.confidence_score)}%
                        </DetailValue>
                      </LetterDetail>
                    </LetterDetails>

                    <LetterSummary>
                      <DetailLabel>AI Summary</DetailLabel>
                      <SummaryText>
                        {letter.ai_summary?.summary || 'No summary available'}
                      </SummaryText>
                    </LetterSummary>

                    {letter.storage_info?.file_storage?.success && (
                      <LetterActions>
                        <DownloadButton 
                          onClick={() => handleDownload(letter.storage_id, letter.filename)}
                        >
                          📄 Download Original PDF
                        </DownloadButton>
                        <FileInfo>
                          <FileInfoText>
                            {Math.round(letter.storage_info.file_storage.file_size / 1024)} KB
                          </FileInfoText>
                          <FileInfoText>
                            {new Date(letter.storage_info.file_storage.upload_timestamp).toLocaleDateString('en-GB')}
                          </FileInfoText>
                        </FileInfo>
                      </LetterActions>
                    )}
                  </LetterCard>
                ))}
              </div>
            )}

            {!loadingLetters && !lettersError && letters.length === 0 && (
              <div style={{ 
                textAlign: 'center', 
                padding: '40px 20px',
                color: colors.textLight,
                fontSize: typography.fontSize.md
              }}>
                📋 No stored letters found. Upload a letter to see it here.
              </div>
            )}
          </>
        )}
      </MainContent>
    </AppContainer>
  );
}

export default App;
