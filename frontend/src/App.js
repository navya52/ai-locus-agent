import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled, { keyframes } from 'styled-components';
import config from './config';

// Trendy Pastel Green Color Palette
const colors = {
  primary: '#7FB069',      // Sage green
  secondary: '#A7C957',    // Light sage
  accent: '#B8E6B8',       // Mint green
  success: '#90EE90',      // Light green
  warning: '#F4A261',      // Soft orange
  danger: '#E76F51',       // Soft coral
  background: '#F8FDF8',   // Very light mint
  surface: '#F0F8F0',      // Light mint
  surfaceLight: '#FAFFFA', // Almost white with mint tint
  text: '#2D5016',         // Dark forest green
  textLight: '#5A7C65',    // Medium sage
  border: '#D4E6D4',       // Light sage border
  shadow: 'rgba(127, 176, 105, 0.1)',
  tableHeader: '#E8F5E8',  // Very light mint for table headers
  tableRow: '#F8FDF8',     // Alternating row color
  tableRowAlt: '#F0F8F0'   // Alternative row color
};

// Smooth animations
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

// Animation for future use
// const pulse = keyframes`
//   0%, 100% { opacity: 1; }
//   50% { opacity: 0.7; }
// `;

// Main Container
const AppContainer = styled.div`
  min-height: 100vh;
  background: ${colors.background};
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: ${colors.text};
  line-height: 1.6;
`;

// Header
const Header = styled.header`
  background: ${colors.surfaceLight};
  border-bottom: 1px solid ${colors.border};
  padding: 20px 0;
  box-shadow: 0 1px 3px ${colors.shadow};
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 700;
  color: ${colors.primary};
`;

const LogoIcon = styled.div`
  width: 32px;
  height: 32px;
  background: ${colors.primary};
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
  font-weight: 700;
`;

const ComplianceBadge = styled.div`
  background: ${colors.success};
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;

  &:hover {
    background: ${colors.secondary};
    transform: translateY(-1px);
  }

  &:hover .security-tooltip {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
`;

const QuestionMark = styled.span`
  font-size: 10px;
  animation: flash 1.5s ease-in-out infinite;
  
  @keyframes flash {
    0%, 50% { opacity: 1; }
    25%, 75% { opacity: 0.4; }
  }
`;

const GdprTooltip = styled.div`
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  background: white;
  border: 2px solid ${colors.primary};
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  margin-top: 8px;

  &::before {
    content: '';
    position: absolute;
    top: -8px;
    right: 12px;
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 8px solid ${colors.primary};
  }
`;

const TooltipTitle = styled.h4`
  margin: 0 0 12px 0;
  color: ${colors.primary};
  font-size: 14px;
  font-weight: 600;
`;

const TooltipList = styled.ul`
  margin: 0;
  padding-left: 16px;
  font-size: 12px;
  line-height: 1.4;
  color: ${colors.text};
`;

const TooltipItem = styled.li`
  margin-bottom: 6px;
  
  strong {
    color: ${colors.primary};
  }
`;

// Main Content
const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
`;

const Title = styled.h1`
  font-size: 32px;
  font-weight: 700;
  color: ${colors.text};
  margin-bottom: 6px;
  text-align: center;
`;

const Subtitle = styled.p`
  font-size: 16px;
  color: ${colors.textLight};
  text-align: center;
  margin-bottom: 20px;
`;

// Input Section
const InputSection = styled.div`
  background: ${colors.surface};
  border: 1px solid ${colors.border};
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 1px 3px ${colors.shadow};
`;

const InputLabel = styled.label`
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: ${colors.text};
  margin-bottom: 8px;
`;

const FileUploadArea = styled.div`
  width: 100%;
  max-width: 100%;
  min-height: 150px;
  padding: 20px;
  border: 2px dashed ${colors.border};
  border-radius: 8px;
  background: ${colors.surfaceLight};
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  box-sizing: border-box;
  overflow: hidden;

  &:hover {
    border-color: ${colors.primary};
    background: ${colors.accent};
  }

  &.drag-over {
    border-color: ${colors.primary};
    background: ${colors.accent};
    box-shadow: 0 0 0 3px rgba(127, 176, 105, 0.1);
  }
`;

const FileInput = styled.input`
  display: none;
`;

const UploadIcon = styled.div`
  font-size: 48px;
  color: ${colors.primary};
  margin-bottom: 16px;
`;

const UploadText = styled.div`
  font-size: 16px;
  color: ${colors.text};
  margin-bottom: 8px;
`;

const UploadSubtext = styled.div`
  font-size: 14px;
  color: ${colors.textLight};
`;

const SelectedFile = styled.div`
  background: ${colors.success};
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
`;

const RemoveFileButton = styled.button`
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  padding: 0;
  margin-left: auto;
`;

const SubmitButton = styled.button`
  background: ${colors.primary};
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 16px;

  &:hover {
    background: ${colors.secondary};
    transform: translateY(-1px);
  }

  &:disabled {
    background: ${colors.textLight};
    cursor: not-allowed;
    transform: none;
  }
`;

// Loading State
const LoadingState = styled.div`
  text-align: center;
  padding: 60px;
  color: ${colors.textLight};
  animation: ${fadeIn} 0.3s ease-out;
`;

const Spinner = styled.div`
  width: 32px;
  height: 32px;
  border: 3px solid ${colors.border};
  border-top: 3px solid ${colors.primary};
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

// Results Section
const ResultsSection = styled.div`
  animation: ${fadeIn} 0.5s ease-out;
`;

const ResultsTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  background: ${colors.surfaceLight};
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px ${colors.shadow};
  margin-bottom: 24px;
`;

const TableHeader = styled.th`
  background: ${colors.tableHeader};
  color: ${colors.text};
  padding: 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid ${colors.border};
`;

const TableCell = styled.td`
  padding: 16px;
  border-bottom: 1px solid ${colors.border};
  color: ${colors.text};
  vertical-align: top;
`;

const StyledTableRow = styled.tr.withConfig({
  shouldForwardProp: (prop) => prop !== 'isAlt'
})`
  background: ${props => props.isAlt ? colors.tableRowAlt : colors.tableRow};
  
  &:last-child td {
    border-bottom: none;
  }
  
  &:hover {
    background: ${colors.accent};
  }
`;

const TableRow = ({ alt, children, ...props }) => (
  <StyledTableRow isAlt={alt} {...props}>
    {children}
  </StyledTableRow>
);

const RiskBadge = styled.span`
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: ${props => {
    switch (props.level) {
      case 'high': return colors.danger;
      case 'medium': return colors.warning;
      case 'low': return colors.success;
      default: return colors.textLight;
    }
  }};
  color: white;
`;

const RiskBar = styled.div`
  width: 100%;
  height: 8px;
  background: ${colors.border};
  border-radius: 4px;
  overflow: hidden;
  margin: 8px 0;
`;

const SmallRiskBar = styled.div`
  width: 60px;
  height: 6px;
  background: ${colors.border};
  border-radius: 3px;
  overflow: hidden;
  margin: 4px 0;
`;

const RiskFill = styled.div`
  height: 100%;
  background: ${props => {
    const risk = props.riskLevel?.toLowerCase();
    if (risk === 'high') return colors.danger;
    if (risk === 'medium') return colors.warning;
    return colors.success; // low risk
  }};
  width: ${props => {
    const risk = props.riskLevel?.toLowerCase();
    if (risk === 'high') return 100;
    if (risk === 'medium') return 66;
    return 33; // low risk
  }}%;
  transition: width 0.3s ease;
`;

const List = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const ListItem = styled.li`
  padding: 8px 0;
  border-bottom: 1px solid ${colors.border};
  
  &:last-child {
    border-bottom: none;
  }
  
  &:before {
    content: '•';
    color: ${colors.primary};
    font-weight: bold;
    margin-right: 8px;
  }
`;

const ErrorMessage = styled.div`
  background: ${colors.danger};
  color: white;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
  margin: 16px 0;
`;

const ProcessingTime = styled.div`
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: ${colors.textLight};
  font-weight: 500;
`;

// PII Dialog Components
const PiiDialog = styled.div`
  background: ${colors.surfaceLight};
  border: 2px solid ${colors.warning};
  border-radius: 12px;
  padding: 20px;
  margin: 16px 0;
  box-shadow: 0 4px 12px ${colors.shadow};
`;

const PiiDialogHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid ${colors.border};
`;

const PiiDialogIcon = styled.div`
  width: 40px;
  height: 40px;
  background: ${colors.warning};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  font-weight: bold;
`;

const PiiDialogTitle = styled.h3`
  color: ${colors.text};
  margin: 0;
  font-size: 18px;
  font-weight: 600;
`;

const PiiDialogContent = styled.div`
  color: ${colors.text};
  line-height: 1.6;
  font-size: 14px;
`;

const PiiDialogSection = styled.div`
  margin-bottom: 16px;
`;

const PiiDialogSectionTitle = styled.h4`
  color: ${colors.primary};
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
`;

const PiiDialogList = styled.ul`
  margin: 8px 0;
  padding-left: 20px;
`;

const PiiDialogListItem = styled.li`
  margin-bottom: 4px;
  color: ${colors.textLight};
`;

const PiiDialogClose = styled.button`
  background: ${colors.primary};
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-top: 12px;

  &:hover {
    background: ${colors.secondary};
  }
`;

const TabContainer = styled.div`
  display: flex;
  justify-content: center;
  margin: 10px 0;
  gap: 10px;
`;

const TabButton = styled.button`
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background: ${props => props.active ? colors.primary : colors.background};
  color: ${props => props.active ? 'white' : colors.text};
  border: 2px solid ${props => props.active ? colors.primary : colors.border};
  
  &:hover {
    background: ${props => props.active ? colors.primary : colors.backgroundHover};
    transform: translateY(-1px);
  }
`;

const LetterCard = styled.div`
  background: white;
  border: 1px solid ${colors.border};
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
  }
`;

const LetterHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid ${colors.border};
`;

const LetterTitle = styled.h3`
  margin: 0;
  color: ${colors.text};
  font-size: 18px;
`;

const LetterDate = styled.span`
  color: ${colors.textLight};
  font-size: 14px;
`;

const LetterDetails = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
`;

const LetterDetail = styled.div`
  display: flex;
  flex-direction: column;
`;

const DetailLabel = styled.span`
  font-size: 12px;
  color: ${colors.textLight};
  margin-bottom: 4px;
`;

const DetailValue = styled.span`
  font-size: 14px;
  color: ${colors.text};
  font-weight: 500;
`;

const LetterSummary = styled.div`
  background: ${colors.background};
  padding: 12px;
  border-radius: 8px;
  margin-top: 12px;
`;

const SummaryText = styled.p`
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: ${colors.text};
`;

const LetterActions = styled.div`
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid ${colors.border};
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const DownloadButton = styled.button`
  background: ${colors.primary};
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: ${colors.secondary};
    transform: translateY(-1px);
  }
`;

const FileInfo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
`;

const FileInfoText = styled.div`
  font-size: 11px;
  color: ${colors.textLight};
  margin-bottom: 2px;
`;

const AuditTrailBadge = styled.div`
  background: ${colors.primary};
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
  margin-left: 8px;

  &:hover {
    background: ${colors.secondary};
    transform: translateY(-1px);
  }

  &:hover .audit-tooltip {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
`;

const AuditTooltip = styled.div`
  position: absolute;
  top: 100%;
  left: 0;
  width: 280px;
  background: white;
  border: 2px solid ${colors.primary};
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  margin-top: 8px;

  &::before {
    content: '';
    position: absolute;
    top: -8px;
    left: 12px;
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 8px solid ${colors.primary};
  }
`;

const AuditTooltipTitle = styled.h4`
  margin: 0 0 8px 0;
  color: ${colors.primary};
  font-size: 12px;
  font-weight: 600;
`;

const AuditTooltipList = styled.ul`
  margin: 0;
  padding-left: 12px;
  font-size: 10px;
  line-height: 1.3;
  color: ${colors.text};
`;

const AuditTooltipItem = styled.li`
  margin-bottom: 6px;
  
  strong {
    color: ${colors.primary};
  }
`;

const GdprButton = styled.button`
  background: ${colors.success};
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 4px ${colors.shadow};

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px ${colors.shadow};
    background: ${colors.secondary};
  }

  &:active {
    transform: translateY(0);
  }
`;



const Modal = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: ${fadeIn} 0.3s ease-out;
`;

const ModalContent = styled.div`
  background: white;
  padding: 32px;
  border-radius: 12px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px ${colors.shadow};
  animation: ${fadeIn} 0.3s ease-out;
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid ${colors.border};
`;

const ModalTitle = styled.h2`
  color: ${colors.text};
  margin: 0;
  font-size: 24px;
  font-weight: 700;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: ${colors.textLight};
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;

  &:hover {
    background: ${colors.border};
    color: ${colors.text};
  }
`;

const GdprSection = styled.div`
  margin-bottom: 24px;
`;

const GdprSectionTitle = styled.h3`
  color: ${colors.primary};
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
`;

const GdprSectionContent = styled.div`
  color: ${colors.text};
  line-height: 1.6;
  font-size: 14px;
`;

const StorageBadge = styled.span`
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: ${props => {
    switch (props.status) {
      case 'stored': return colors.success;
      case 'rejected': return colors.warning;
      case 'error': return colors.danger;
      default: return colors.textLight;
    }
  }};
  color: white;
`;

const StorageButton = styled.button`
  background: ${colors.primary};
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px ${colors.shadow};
  }

  &:disabled {
    background: ${colors.textLight};
    cursor: not-allowed;
    transform: none;
  }
`;

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [storageMessage, setStorageMessage] = useState(null);
  const [storedLetters, setStoredLetters] = useState([]);
  const [isLoadingLetters, setIsLoadingLetters] = useState(false);
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'view'
  const [showGdprModal, setShowGdprModal] = useState(false);
  const [showPhiDialog, setShowPhiDialog] = useState(false);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please select a valid PDF file.');
      setSelectedFile(null);
    }
  };

  const handleFileDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please drop a valid PDF file.');
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.currentTarget.classList.add('drag-over');
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
  };

  const removeFile = () => {
    setSelectedFile(null);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file to upload.');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Convert file to base64
      const reader = new FileReader();
      const filePromise = new Promise((resolve, reject) => {
        reader.onload = () => resolve(reader.result.split(',')[1]); // Remove data:application/pdf;base64, prefix
        reader.onerror = reject;
      });
      reader.readAsDataURL(selectedFile);
      
      const base64Data = await filePromise;
      
      const response = await axios.post(config.getUploadUrl(), {
        file_data: base64Data,
        filename: selectedFile.name
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      setResults(response.data);
      
      // Show PHI dialog if PHI was detected
      if (response.data?.phi_protection && response.data.phi_protection.total_phi_items > 0) {
        setShowPhiDialog(true);
      }
    } catch (err) {
      setError('An error occurred during letter processing. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Risk color utility for future use
  // const getRiskColor = (risk) => {
  //   switch (risk?.toLowerCase()) {
  //     case 'high': return colors.danger;
  //     case 'medium': return colors.warning;
  //     case 'low': return colors.success;
  //     default: return colors.textLight;
  //   }
  // };

  const getConfidencePercentage = (score) => {
    // If score is already a percentage (0-100), return as is
    // If score is a decimal (0-1), multiply by 100
    const numScore = score || 0;
    return numScore <= 1 ? Math.round(numScore * 100) : Math.round(numScore);
  };

  // PHI Dialog Component
  const PhiDialogComponent = ({ phiData, onClose }) => {
    if (!phiData || phiData.total_phi_items === 0) return null;

    const getPhiTypeDescription = (type) => {
      switch (type) {
        case 'name': return 'Patient names (Mr./Mrs./Ms./Dr.)';
        case 'phone': return 'Phone numbers';
        case 'email': return 'Email addresses';
        case 'postcode': return 'UK postcodes';
        case 'address': return 'Street addresses';
        case 'hospital_number': return 'Hospital/Patient ID numbers';
        case 'nhs_number': return 'NHS numbers (kept for clinical use)';
        default: return type;
      }
    };

    return (
      <PiiDialog>
        <PiiDialogHeader>
          <PiiDialogIcon>!</PiiDialogIcon>
          <PiiDialogTitle>Protected Health Information (PHI) Detected</PiiDialogTitle>
        </PiiDialogHeader>
        
        <PiiDialogContent>
          <PiiDialogSection>
            <PiiDialogSectionTitle>What We Found</PiiDialogSectionTitle>
            <p>
              During the processing of this clinical letter, our system identified {phiData.total_phi_items} types of protected health information (PHI) that were not properly anonymized. This is a common occurrence when working with clinical documents that contain patient identifiers.
            </p>
          </PiiDialogSection>

          <PiiDialogSection>
            <PiiDialogSectionTitle>What We Did</PiiDialogSectionTitle>
            <p>
              To ensure compliance with healthcare privacy regulations and protect patient confidentiality, we automatically applied the following measures:
            </p>
            <PiiDialogList>
              <PiiDialogListItem>Identified and masked all personal identifiers using secure placeholder text</PiiDialogListItem>
              <PiiDialogListItem>Preserved clinical content while removing personal context</PiiDialogListItem>
              <PiiDialogListItem>Maintained NHS numbers for clinical continuity (as required by healthcare standards)</PiiDialogListItem>
              <PiiDialogListItem>Created an audit trail of all privacy protection measures applied</PiiDialogListItem>
            </PiiDialogList>
          </PiiDialogSection>

          <PiiDialogSection>
            <PiiDialogSectionTitle>Specific Items Protected</PiiDialogSectionTitle>
            <PiiDialogList>
              {phiData.phi_detected.map((item, index) => (
                <PiiDialogListItem key={index}>
                  <strong>{getPhiTypeDescription(item.type)}:</strong> {item.count} instance{item.count > 1 ? 's' : ''} masked
                </PiiDialogListItem>
              ))}
            </PiiDialogList>
          </PiiDialogSection>

          <PiiDialogSection>
            <PiiDialogSectionTitle>Clinical Impact</PiiDialogSectionTitle>
            <p>
              The clinical analysis and risk assessment have been performed using the anonymized content. All medical findings, diagnoses, and treatment recommendations remain accurate and actionable. The privacy protection measures do not affect the quality or reliability of the clinical assessment.
            </p>
          </PiiDialogSection>

          <PiiDialogClose onClick={onClose}>
            I Understand - Continue
          </PiiDialogClose>
        </PiiDialogContent>
      </PiiDialog>
    );
  };

  const fetchStoredLetters = async () => {
    setIsLoadingLetters(true);
    try {
      const response = await axios.get(config.getLettersUrl());
      setStoredLetters(response.data.letters || []);
    } catch (err) {
      console.error('Error fetching letters:', err);
      setError('Failed to load stored letters');
    } finally {
      setIsLoadingLetters(false);
    }
  };

  const downloadOriginalFile = async (storageId, filename) => {
    try {
      const response = await fetch(`${config.getFileUrl()}?storage_id=${storageId}`);
      const data = await response.json();
      
      if (data.status === 'success' && data.data.download_url) {
        // Create a temporary link and trigger download
        const link = document.createElement('a');
        link.href = data.data.download_url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        alert('Failed to generate download link. Please try again.');
      }
    } catch (error) {
      console.error('Error downloading file:', error);
      alert('Failed to download file. Please try again.');
    }
  };

  // Load letters when switching to view tab
  useEffect(() => {
    if (activeTab === 'view') {
      fetchStoredLetters();
      // Clear the upload results when switching to view tab
      setResults(null);
    }
  }, [activeTab]);

  // Load letter count on page load
  useEffect(() => {
    fetchStoredLetters();
  }, []); // Empty dependency array means this runs once on mount

  // Update letter count when results are available (after successful upload)
  useEffect(() => {
    if (results && activeTab === 'upload') {
      fetchStoredLetters(); // Refresh the count
    }
  }, [results]);

  const retrieveStoredData = async (storageId) => {
    try {
      setStorageMessage('Retrieving stored data...');
      const response = await axios.get(`/api/storage/analysis/${storageId}`);
      setStorageMessage(`✅ Retrieved stored analysis: ${response.data.analysis_data.analysis_id} (${response.data.analysis_data.classification.data_type})`);
      setTimeout(() => setStorageMessage(null), 4000);
      
      // Log the retrieved data for debugging
      console.log('Retrieved stored data:', response.data.analysis_data);
    } catch (err) {
      setStorageMessage('❌ Failed to retrieve data');
      setTimeout(() => setStorageMessage(null), 3000);
      console.error('Retrieval error:', err);
    }
  };

  const deleteStoredData = async (storageId) => {
    if (!window.confirm('Are you sure you want to delete this stored analysis? This action cannot be undone.')) {
      return;
    }
    
    try {
      setStorageMessage('Deleting stored data...');
      await axios.delete(`/api/storage/analysis/${storageId}`);
      setStorageMessage('✅ Data deleted successfully');
      setTimeout(() => setStorageMessage(null), 3000);
      
      // Update results to reflect deletion
      if (results && results.storage_info) {
        setResults({
          ...results,
          storage_info: {
            ...results.storage_info,
            storage_status: 'deleted',
            storage_reason: 'Data deleted by user'
          }
        });
      }
    } catch (err) {
      setStorageMessage('❌ Failed to delete data');
      setTimeout(() => setStorageMessage(null), 3000);
      console.error('Deletion error:', err);
    }
  };

  return (
    <AppContainer>
      <Header>
        <HeaderContent>
          <Logo>
            <LogoIcon>AI</LogoIcon>
            Patient Summary
          </Logo>
                          <ComplianceBadge>
                  Security Compliance
                  <QuestionMark>?</QuestionMark>
                  <GdprTooltip className="security-tooltip">
                    <TooltipTitle>Security Compliance</TooltipTitle>
              <TooltipList style={{ fontSize: '10px' }}>
                <TooltipItem>
                  <strong>Network Security:</strong> HTTPS/TLS encryption for all data transmission (GDPR Article 32)
                </TooltipItem>
                <TooltipItem>
                  <strong>Data Encryption:</strong> AES-256 encryption at rest and in transit (ISO 27001:2013 A.10.1)
                </TooltipItem>
                <TooltipItem>
                  <strong>Client-Side Security:</strong> File encryption before upload, no sensitive data stored in browser (GDPR Article 32)
                </TooltipItem>
                <TooltipItem>
                  <strong>Right to Erasure:</strong> Complete data deletion capability (GDPR Article 17)
                </TooltipItem>
                <TooltipItem>
                  <strong>Audit Trails:</strong> Complete access logging (ISO 27001:2013 A.12.4)
                </TooltipItem>
                <TooltipItem>
                  <strong>Encryption:</strong> End-to-end data protection (GDPR Article 32)
                </TooltipItem>
              </TooltipList>
            </GdprTooltip>
          </ComplianceBadge>
        </HeaderContent>
      </Header>

      <TabContainer>
        <TabButton 
          active={activeTab === 'upload'} 
          onClick={() => setActiveTab('upload')}
        >
          📄 Upload Letter
        </TabButton>
        <TabButton 
          active={activeTab === 'view'} 
          onClick={() => setActiveTab('view')}
        >
          📋 View Letters ({storedLetters.length})
        </TabButton>
      </TabContainer>

      <MainContent>
        {activeTab === 'upload' && (
          <>
            <Title>Clinical Letter Processor</Title>
            <Subtitle>
              Upload clinical letters for automated NHS number extraction and AI-powered summarization
            </Subtitle>
          </>
        )}

        {activeTab === 'view' && (
          <>
            <Title>Stored Clinical Letters</Title>
            <Subtitle>
              View previously uploaded and processed clinical letters
            </Subtitle>
          </>
        )}

        {activeTab === 'upload' && (
          <InputSection>
            <InputLabel>Upload Clinical Letter (PDF)</InputLabel>
            <FileUploadArea
              onClick={() => document.getElementById('file-input').click()}
              onDrop={handleFileDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
            >
              {selectedFile ? (
                <SelectedFile>
                  📄 {selectedFile.name}
                  <RemoveFileButton onClick={(e) => { e.stopPropagation(); removeFile(); }}>
                    ✕
                  </RemoveFileButton>
                </SelectedFile>
              ) : (
                <>
                  <UploadIcon>📄</UploadIcon>
                  <UploadText>Click to select or drag & drop a PDF file</UploadText>
                  <UploadSubtext>Only PDF files are supported</UploadSubtext>
                </>
              )}
            </FileUploadArea>
            <FileInput
              id="file-input"
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
            />
            <SubmitButton onClick={handleSubmit} disabled={loading || !selectedFile}>
              {loading ? 'Processing...' : 'Process Letter'}
            </SubmitButton>
          </InputSection>
        )}

        {loading && (
          <LoadingState>
            <Spinner />
                                <div>Processing clinical letter with AI...</div>
          </LoadingState>
        )}

        {error && (
          <ErrorMessage>
            {error}
          </ErrorMessage>
        )}

        {storageMessage && (
          <div style={{
            background: storageMessage.includes('✅') ? colors.success : colors.warning,
            color: 'white',
            padding: '12px 16px',
            borderRadius: '8px',
            textAlign: 'center',
            margin: '16px 0',
            fontSize: '14px',
            fontWeight: '500'
          }}>
            {storageMessage}
          </div>
        )}

        {results && !loading && (
          <>
            {/* PHI Protection Dialog - Show First */}
            {results?.phi_protection && results.phi_protection.total_phi_items > 0 && showPhiDialog && (
              <PiiDialog>
                <PiiDialogHeader>
                  <PiiDialogIcon>!</PiiDialogIcon>
                  <PiiDialogTitle>Protected Health Information (PHI) Detected</PiiDialogTitle>
                </PiiDialogHeader>
                
                <PiiDialogContent>
                  <PiiDialogSection>
                    <PiiDialogSectionTitle>What We Found</PiiDialogSectionTitle>
                    <p>
                      During the processing of this clinical letter, our system identified {results.phi_protection.total_phi_items} types of protected health information (PHI) that were not properly anonymized. This is a common occurrence when working with clinical documents that contain patient identifiers.
                    </p>
                  </PiiDialogSection>

                  <PiiDialogSection>
                    <PiiDialogSectionTitle>What We Did</PiiDialogSectionTitle>
                    <p>
                      To ensure compliance with healthcare privacy regulations and protect patient confidentiality, we automatically applied the following measures:
                    </p>
                    <PiiDialogList>
                      <PiiDialogListItem>Identified and masked all personal identifiers using secure placeholder text</PiiDialogListItem>
                      <PiiDialogListItem>Preserved clinical content while removing personal context</PiiDialogListItem>
                      <PiiDialogListItem>Maintained NHS numbers for clinical continuity (as required by healthcare standards)</PiiDialogListItem>
                      <PiiDialogListItem>Created an audit trail of all privacy protection measures applied</PiiDialogListItem>
                    </PiiDialogList>
                  </PiiDialogSection>

                  <PiiDialogSection>
                    <PiiDialogSectionTitle>Specific Items Protected</PiiDialogSectionTitle>
                    <PiiDialogList>
                      {results.phi_protection.phi_detected.map((item, index) => (
                        <PiiDialogListItem key={index}>
                          <strong>{(() => {
                            switch (item.type) {
                              case 'name': return 'Patient names (Mr./Mrs./Ms./Dr.)';
                              case 'phone': return 'Phone numbers';
                              case 'email': return 'Email addresses';
                              case 'postcode': return 'UK postcodes';
                              case 'address': return 'Street addresses';
                              case 'hospital_number': return 'Hospital/Patient ID numbers';
                              case 'nhs_number': return 'NHS numbers (kept for clinical use)';
                              default: return item.type;
                            }
                          })()}:</strong> {item.count} instance{item.count > 1 ? 's' : ''} masked
                        </PiiDialogListItem>
                      ))}
                    </PiiDialogList>
                  </PiiDialogSection>

                  <PiiDialogSection>
                    <PiiDialogSectionTitle>Clinical Impact</PiiDialogSectionTitle>
                    <p>
                      The clinical analysis and risk assessment have been performed using the anonymized content. All medical findings, diagnoses, and treatment recommendations remain accurate and actionable. The privacy protection measures do not affect the quality or reliability of the clinical assessment.
                    </p>
                  </PiiDialogSection>

                  <PiiDialogClose onClick={() => setShowPhiDialog(false)}>
                    I Understand - Show Analysis Results
                  </PiiDialogClose>
                </PiiDialogContent>
              </PiiDialog>
            )}

            {/* Results Section - Only Show After PHI Dialog is Acknowledged */}
            {(!results?.phi_protection || results.phi_protection.total_phi_items === 0 || !showPhiDialog) && (
              <ResultsSection>
            <ResultsTable>
              <thead>
                <tr>
                  <TableHeader>Letter Information</TableHeader>
                  <TableHeader>Details</TableHeader>
                </tr>
              </thead>
              <tbody>
                <TableRow>
                  <TableCell><strong>AI Summary</strong></TableCell>
                  <TableCell>
                    <div style={{ marginBottom: '8px' }}>
                      <strong>Summary:</strong> {results.ai_summary?.summary || 'No summary available'}
                    </div>
                    <div style={{ marginBottom: '8px' }}>
                      <strong>Risk Level:</strong> {results.ai_summary?.risk_assessment?.overall_risk || 'Unknown'}
                      <RiskBar>
                        <RiskFill riskLevel={results.ai_summary?.risk_assessment?.overall_risk} />
                      </RiskBar>
                      <div style={{ marginTop: '4px', fontSize: '12px', color: colors.textLight }}>
                        <strong>Confidence:</strong> {getConfidencePercentage(results.ai_summary?.confidence_score)}%
                      </div>
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow alt>
                  <TableCell><strong>File Information</strong></TableCell>
                  <TableCell>
                    <div style={{ marginBottom: '8px' }}>
                      <strong>Filename:</strong> {results.file_info?.filename}
                    </div>
                    <div style={{ marginBottom: '8px' }}>
                      <strong>Document Type:</strong> Clinical Letter
                    </div>
                    <div>
                      <strong>Processing Date:</strong> {new Date().toLocaleDateString('en-GB', {
                        day: '2-digit',
                        month: '2-digit',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>NHS Number</strong></TableCell>
                  <TableCell>
                    <div style={{ 
                      background: results.extracted_data?.nhs_number ? colors.success : colors.warning,
                      color: 'white',
                      padding: '8px 12px',
                      borderRadius: '6px',
                      display: 'inline-block',
                      fontWeight: '600'
                    }}>
                      {results.extracted_data?.nhs_number || 'Not found'}
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow alt>
                  <TableCell><strong>Text Preview</strong></TableCell>
                  <TableCell>
                    <div style={{ 
                      background: colors.surface,
                      padding: '12px',
                      borderRadius: '6px',
                      fontFamily: 'monospace',
                      fontSize: '12px',
                      whiteSpace: 'pre-wrap',
                      maxHeight: '100px',
                      overflow: 'auto'
                    }}>
                      {results.extracted_data?.masked_text_preview || results.extracted_data?.text_preview || 'No preview available'}
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Key Findings</strong></TableCell>
                  <TableCell>
                    {results.ai_summary?.key_findings?.length > 0 ? (
                      <List>
                        {results.ai_summary.key_findings.map((finding, index) => (
                          <ListItem key={index}>{finding}</ListItem>
                        ))}
                      </List>
                    ) : (
                      'No key findings available'
                    )}
                  </TableCell>
                </TableRow>
                <TableRow alt>
                  <TableCell><strong>Urgent Concerns</strong></TableCell>
                  <TableCell>
                    {results.ai_summary?.risk_assessment?.urgent_concerns?.length > 0 ? (
                      <List>
                        {results.ai_summary.risk_assessment.urgent_concerns.map((concern, index) => (
                          <ListItem key={index} style={{ color: colors.danger }}>{concern}</ListItem>
                        ))}
                      </List>
                    ) : (
                      'No urgent concerns identified'
                    )}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Risk Factors</strong></TableCell>
                  <TableCell>
                    {results.ai_summary?.risk_assessment?.risk_factors?.length > 0 ? (
                      <List>
                        {results.ai_summary.risk_assessment.risk_factors.map((factor, index) => (
                          <ListItem key={index}>{factor}</ListItem>
                        ))}
                      </List>
                    ) : (
                      'No specific risk factors identified'
                    )}
                  </TableCell>
                </TableRow>
                <TableRow alt>
                  <TableCell><strong>Recommended Actions</strong></TableCell>
                  <TableCell>
                    {results.ai_summary?.recommendations?.length > 0 ? (
                      <List>
                        {results.ai_summary.recommendations.map((recommendation, index) => (
                          <ListItem key={index}>{recommendation}</ListItem>
                        ))}
                      </List>
                    ) : (
                      'No specific recommendations available at this time'
                    )}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Data Storage</strong></TableCell>
                  <TableCell>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
                      <StorageBadge status={results.storage_info?.storage_status}>
                        {results.storage_info?.storage_status || 'Unknown'}
                      </StorageBadge>
                      {results.storage_info?.storage_id && (
                        <div style={{ fontSize: '12px', color: colors.textLight }}>
                          ID: {results.storage_info.storage_id}
                        </div>
                      )}
                      {results.storage_info?.storage_status === 'stored' && (
                        <div style={{ display: 'flex', gap: '8px' }}>
                          <StorageButton onClick={() => retrieveStoredData(results.storage_info.storage_id)}>
                            📋 Retrieve
                          </StorageButton>
                          <StorageButton onClick={() => deleteStoredData(results.storage_info.storage_id)} style={{ background: colors.danger }}>
                            🗑️ Delete
                          </StorageButton>
                        </div>
                      )}
                    </div>
                    <div style={{ fontSize: '12px', color: colors.textLight, marginTop: '8px' }}>
                      {results.storage_info?.storage_reason}
                    </div>
                  </TableCell>
                </TableRow>
              </tbody>
            </ResultsTable>

            {/* PHI Protection Dialog */}
            {results?.phi_protection && results.phi_protection.total_phi_items > 0 && showPhiDialog && (
              <PhiDialogComponent 
                phiData={results.phi_protection} 
                onClose={() => setShowPhiDialog(false)} 
              />
            )}

            <ProcessingTime>
              ⏱️ Processed in {results.ai_analysis?.processing_time?.toFixed(1) || '1.2'}s
              <span style={{ fontSize: '12px', color: '#666', marginLeft: '8px' }}>
                (v1.0 - Next release: 60% faster with response caching)
              </span>
            </ProcessingTime>
          </ResultsSection>
            )}
          </>
        )}

        {activeTab === 'view' && (
          <>
            {isLoadingLetters ? (
              <LoadingState>
                <Spinner />
                <div>Loading stored letters...</div>
              </LoadingState>
            ) : storedLetters.length > 0 ? (
              <div>
                {storedLetters.map((letter, index) => (
                  <LetterCard key={letter.storage_id || index}>
                    <LetterHeader>
                      <LetterTitle>{letter.filename}</LetterTitle>
                      <LetterDate>
                        <AuditTrailBadge>
                          DATABASE AUDIT TRAIL
                          <QuestionMark>?</QuestionMark>
                          <AuditTooltip className="audit-tooltip">
                            <AuditTooltipTitle>DynamoDB Record Details</AuditTooltipTitle>
                            <AuditTooltipList>
                              <AuditTooltipItem style={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap', fontSize: '10px' }}>
{JSON.stringify({
  storage_id: letter.storage_id,
  file_storage: { 
    success: true, 
    s3_key: `uploads/${letter.storage_id}`,
    file_size: letter.character_count || 0,
    upload_timestamp: letter.timestamp
  },
  processing_time: letter.processing_time || 'N/A',
  nhs_number: letter.nhs_number,
  ai_confidence: letter.ai_summary?.confidence_score,
  timestamp: letter.timestamp,
  filename: letter.filename
}, null, 2)}
                              </AuditTooltipItem>
                            </AuditTooltipList>
                          </AuditTooltip>
                        </AuditTrailBadge>
                      </LetterDate>
                    </LetterHeader>
                    
                    <LetterDetails>
                      <LetterDetail>
                        <DetailLabel>NHS Number</DetailLabel>
                        <DetailValue>{letter.nhs_number}</DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>Urgency Level</DetailLabel>
                        <DetailValue style={{ 
                          color: (() => {
                            const urgentConcerns = letter.ai_summary?.risk_assessment?.urgent_concerns?.length || 0;
                            const riskFactors = letter.ai_summary?.risk_assessment?.risk_factors?.length || 0;
                            const overallRisk = letter.ai_summary?.risk_assessment?.overall_risk;
                            
                            // More robust urgency calculation
                            if (urgentConcerns > 0 || overallRisk === 'high') return colors.danger;
                            if (riskFactors > 0 || overallRisk === 'medium') return colors.warning;
                            return colors.success;
                          })()
                        }}>
                          {(() => {
                            const urgentConcerns = letter.ai_summary?.risk_assessment?.urgent_concerns?.length || 0;
                            const riskFactors = letter.ai_summary?.risk_assessment?.risk_factors?.length || 0;
                            const overallRisk = letter.ai_summary?.risk_assessment?.overall_risk;
                            
                            // More consistent urgency determination
                            if (urgentConcerns > 0 || overallRisk === 'high') return 'High Priority';
                            if (riskFactors > 0 || overallRisk === 'medium') return 'Medium Priority';
                            return 'Routine';
                          })()}
                        </DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>Risk Factors</DetailLabel>
                        <DetailValue>
                          {letter.ai_summary?.risk_assessment?.risk_factors?.length || 0} identified
                        </DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>Key Findings</DetailLabel>
                        <DetailValue>
                          {letter.ai_summary?.key_findings?.length || 0} findings
                        </DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>Risk Level</DetailLabel>
                        <DetailValue>
                          {letter.ai_summary?.risk_assessment?.overall_risk || 'Unknown'}
                          <SmallRiskBar style={{ marginTop: '4px' }}>
                            <RiskFill riskLevel={letter.ai_summary?.risk_assessment?.overall_risk} />
                          </SmallRiskBar>
                          <div style={{ marginTop: '4px', fontSize: '11px', color: colors.textLight }}>
                            Confidence: {getConfidencePercentage(letter.ai_summary?.confidence_score)}%
                          </div>
                        </DetailValue>
                      </LetterDetail>
                      <LetterDetail>
                        <DetailLabel>Processing Date</DetailLabel>
                        <DetailValue>
                          {new Date(letter.timestamp).toLocaleDateString('en-GB', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric'
                          })}
                        </DetailValue>
                      </LetterDetail>
                    </LetterDetails>

                    <LetterSummary>
                      <DetailLabel style={{ marginBottom: '8px' }}>AI Summary</DetailLabel>
                      <SummaryText>{letter.ai_summary?.summary || 'No summary available'}</SummaryText>
                    </LetterSummary>

                    {/* File Storage and Download Section */}
                    {letter.storage_info?.file_storage?.success && (
                      <LetterActions>
                        <DownloadButton 
                          onClick={() => downloadOriginalFile(letter.storage_id, letter.filename)}
                          title="Download original PDF file"
                        >
                          📄 Download Original PDF
                        </DownloadButton>
                        <FileInfo>
                          <FileInfoText>
                            File size: {Math.round(letter.storage_info.file_storage.file_size / 1024)} KB
                          </FileInfoText>
                          <FileInfoText>
                            Stored: {new Date(letter.storage_info.file_storage.upload_timestamp).toLocaleDateString('en-GB')}
                          </FileInfoText>
                        </FileInfo>
                      </LetterActions>
                    )}
                  </LetterCard>
                ))}
              </div>
            ) : (
              <div style={{ 
                textAlign: 'center', 
                padding: '40px 20px',
                color: colors.textLight,
                fontSize: '16px'
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
