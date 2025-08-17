import React from 'react';
import styled from 'styled-components';
import { colors, typography, spacing, borderRadius } from '../../styles/theme';
import { RISK_LEVELS } from '../../constants';

const ResultsSection = styled.div`
  margin-top: ${spacing.xl};
`;

const ResultsTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: ${borderRadius.lg};
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const TableHeader = styled.th`
  background: ${colors.tableHeader};
  padding: ${spacing.md};
  text-align: left;
  font-weight: ${typography.fontWeight.semibold};
  color: ${colors.text};
  border-bottom: 1px solid ${colors.border};
`;

const TableCell = styled.td`
  padding: ${spacing.md};
  border-bottom: 1px solid ${colors.border};
  color: ${colors.text};
`;

const StyledTableRow = styled.tr.withConfig({
  shouldForwardProp: (prop) => prop !== 'isEven'
})`
  background: ${props => props.isEven ? colors.tableRow : 'white'};
  
  &:hover {
    background: ${colors.background};
  }
`;

const RiskBadge = styled.span`
  padding: 4px 12px;
  border-radius: ${borderRadius.xl};
  font-size: ${typography.fontSize.xs};
  font-weight: ${typography.fontWeight.semibold};
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: ${props => {
    switch (props.riskLevel) {
      case RISK_LEVELS.HIGH: return colors.danger;
      case RISK_LEVELS.MEDIUM: return colors.warning;
      case RISK_LEVELS.LOW: return colors.success;
      default: return colors.textLight;
    }
  }};
  color: white;
`;

const RiskBar = styled.div`
  width: 100px;
  height: 8px;
  background: ${colors.border};
  border-radius: 4px;
  overflow: hidden;
  margin-top: 4px;
`;

const RiskFill = styled.div`
  height: 100%;
  background: ${props => {
    switch (props.riskLevel) {
      case RISK_LEVELS.HIGH: return colors.danger;
      case RISK_LEVELS.MEDIUM: return colors.warning;
      case RISK_LEVELS.LOW: return colors.success;
      default: return colors.textLight;
    }
  }};
  width: ${props => {
    switch (props.riskLevel) {
      case RISK_LEVELS.HIGH: return '100%';
      case RISK_LEVELS.MEDIUM: return '60%';
      case RISK_LEVELS.LOW: return '30%';
      default: return '0%';
    }
  }};
  transition: width 0.3s ease;
`;

const List = styled.ul`
  margin: 0;
  padding-left: 16px;
  font-size: ${typography.fontSize.sm};
`;

const ListItem = styled.li`
  margin-bottom: 2px;
  color: ${colors.textLight};
`;

const ProcessingTime = styled.div`
  font-size: ${typography.fontSize.xs};
  color: ${colors.textLight};
  margin-top: ${spacing.sm};
`;

const ResultsTableComponent = ({ results }) => {
  if (!results) return null;

  const getConfidencePercentage = (score) => {
    const numScore = score || 0;
    return numScore <= 1 ? Math.round(numScore * 100) : Math.round(numScore);
  };

  return (
    <ResultsSection>
      <ResultsTable>
        <thead>
          <tr>
            <TableHeader>Metric</TableHeader>
            <TableHeader>Value</TableHeader>
            <TableHeader>Details</TableHeader>
          </tr>
        </thead>
        <tbody>
          <StyledTableRow>
            <TableCell>File Information</TableCell>
            <TableCell>
              <strong>{results.file_info?.filename}</strong>
              <br />
              {results.file_info?.word_count} words, {results.file_info?.character_count} characters
            </TableCell>
            <TableCell>
              File size: {Math.round(results.file_info?.file_size_bytes / 1024)} KB
            </TableCell>
          </StyledTableRow>

          <StyledTableRow isEven>
            <TableCell>NHS Number</TableCell>
            <TableCell>
              {results.extracted_data?.nhs_number || 'Not found'}
            </TableCell>
            <TableCell>
              {results.extracted_data?.nhs_number ? 'Extracted successfully' : 'No NHS number detected'}
            </TableCell>
          </StyledTableRow>

          <StyledTableRow>
            <TableCell>Risk Assessment</TableCell>
            <TableCell>
              <RiskBadge riskLevel={results.ai_summary?.risk_assessment?.overall_risk}>
                {results.ai_summary?.risk_assessment?.overall_risk || 'Unknown'}
              </RiskBadge>
              <RiskBar>
                <RiskFill riskLevel={results.ai_summary?.risk_assessment?.overall_risk} />
              </RiskBar>
            </TableCell>
            <TableCell>
              Confidence: {getConfidencePercentage(results.ai_summary?.confidence_score)}%
            </TableCell>
          </StyledTableRow>

          <StyledTableRow isEven>
            <TableCell>Urgent Concerns</TableCell>
            <TableCell>
              {results.ai_summary?.risk_assessment?.urgent_concerns?.length || 0} items
            </TableCell>
            <TableCell>
              <List>
                {results.ai_summary?.risk_assessment?.urgent_concerns?.map((concern, index) => (
                  <ListItem key={index}>{concern}</ListItem>
                )) || <ListItem>None identified</ListItem>}
              </List>
            </TableCell>
          </StyledTableRow>

          <StyledTableRow>
            <TableCell>Risk Factors</TableCell>
            <TableCell>
              {results.ai_summary?.risk_assessment?.risk_factors?.length || 0} factors
            </TableCell>
            <TableCell>
              <List>
                {results.ai_summary?.risk_assessment?.risk_factors?.map((factor, index) => (
                  <ListItem key={index}>{factor}</ListItem>
                )) || <ListItem>None identified</ListItem>}
              </List>
            </TableCell>
          </StyledTableRow>

          <StyledTableRow isEven>
            <TableCell>Key Findings</TableCell>
            <TableCell>
              {results.ai_summary?.key_findings?.length || 0} findings
            </TableCell>
            <TableCell>
              <List>
                {results.ai_summary?.key_findings?.map((finding, index) => (
                  <ListItem key={index}>{finding}</ListItem>
                )) || <ListItem>No findings</ListItem>}
              </List>
            </TableCell>
          </StyledTableRow>

          <StyledTableRow>
            <TableCell>PHI Protection</TableCell>
            <TableCell>
              {results.phi_protection?.total_phi_items || 0} items detected
            </TableCell>
            <TableCell>
              {results.phi_protection?.privacy_compliant ? '✅ Compliant' : '❌ Non-compliant'}
            </TableCell>
          </StyledTableRow>

          <StyledTableRow isEven>
            <TableCell>Processing</TableCell>
            <TableCell>
              {results.processing_time}s
            </TableCell>
            <TableCell>
              <ProcessingTime>
                Completed at {new Date(results.processing_timestamp).toLocaleTimeString()}
              </ProcessingTime>
            </TableCell>
          </StyledTableRow>
        </tbody>
      </ResultsTable>
    </ResultsSection>
  );
};

export default ResultsTableComponent;
