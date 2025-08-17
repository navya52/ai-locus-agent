import React from 'react';
import styled from 'styled-components';
import { colors, typography, shadows } from '../../styles/theme';

const HeaderContainer = styled.header`
  background: ${colors.surfaceLight};
  border-bottom: 1px solid ${colors.border};
  padding: 20px 0;
  box-shadow: ${shadows.sm};
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
  font-size: ${typography.fontSize.xl};
  font-weight: ${typography.fontWeight.bold};
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
  font-weight: ${typography.fontWeight.bold};
`;

const ComplianceBadge = styled.div`
  background: ${colors.success};
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: ${typography.fontSize.xs};
  font-weight: ${typography.fontWeight.semibold};
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: ${shadows.md};
  }
`;

const QuestionMark = styled.span`
  width: 16px;
  height: 16px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: ${typography.fontWeight.bold};
`;

const GdprTooltip = styled.div`
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 1px solid ${colors.border};
  border-radius: 8px;
  padding: 16px;
  width: 300px;
  box-shadow: ${shadows.lg};
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;

  ${ComplianceBadge}:hover & {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
`;

const TooltipTitle = styled.h4`
  color: ${colors.primary};
  margin: 0 0 8px 0;
  font-size: ${typography.fontSize.sm};
  font-weight: ${typography.fontWeight.semibold};
`;

const TooltipList = styled.ul`
  margin: 0;
  padding-left: 16px;
  color: ${colors.text};
  font-size: ${typography.fontSize.xs};
  line-height: 1.4;
`;

const TooltipItem = styled.li`
  margin-bottom: 4px;
`;

const Header = () => {
  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo>
          <LogoIcon>AI</LogoIcon>
          AI Locus Agent
        </Logo>
        
        <ComplianceBadge>
          <QuestionMark>?</QuestionMark>
          GDPR Compliant
          <GdprTooltip>
            <TooltipTitle>Privacy & Compliance</TooltipTitle>
            <TooltipList>
              <TooltipItem>All data processed securely</TooltipItem>
              <TooltipItem>PHI detection & masking</TooltipItem>
              <TooltipItem>Audit trail maintained</TooltipItem>
              <TooltipItem>Data retention policies</TooltipItem>
            </TooltipList>
          </GdprTooltip>
        </ComplianceBadge>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;
