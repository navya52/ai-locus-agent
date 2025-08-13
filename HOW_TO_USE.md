# How to Use AI Locus Agent

A comprehensive guide to using the AI Locus Agent system for clinical letter processing and analysis.

## Live Demo

**Access the application**: http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com

> **Note**: Only HTTP works for now, had to rollback HTTPS last minute due to CloudFront's free plan not being suitable. Click on "proceed anyway"

## Getting Started

### Step 1: Access the Application
2. Navigate to: http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com
 (Only HTTP works for now, had to rollback HTTPS last minute due to CloudFront's free plan not being suitable)
3. You'll see the main interface with two tabs:
   - **Upload Letter** - For processing new letters
   - **View Letters** - For viewing previously processed letters (letters already exist from me testing)

### Step 2: Upload Your First Letter
1. Click on the **" Upload Letter"** tab
2. Click **"Choose File"** or drag and drop a PDF clinical letter
3. Click **"Upload and Analyze"**
4. Wait for processing (typically 1-2 seconds)
5. View the results showing:
   - NHS number extraction
   - AI-generated summary
   - Risk assessment
   - Key findings and recommendations

### Try the GDPR Compliance Hover Tooltip on the top right corner
1. **Look for the "GDPR COMPLIANT"** badge (green button with checkmark) in the top right, a detailed tooltip will appear showing cool stuff

### Try the Database Audit Trail Hover Tooltip
1. **In the " View Letters"** tab
2. **Look for "DATABASE AUDIT TRAIL ?"** button (next to letter date)
3. **Hover over the button** - a tooltip will appear showing:
  
## Also added a demo feature for edge case input - PHI Detection & Masking

**Testing PHI Protection:**
1. **Upload the "Sample_File_with_PHI.pdf" file from the project's root directory** 
2. **A PHI dialog will appear** explaining what was detected and masked
3. **The system only flags actual names** - generic terms like "LONDON" are ignored
4. **PHI masking happens before AI analysis** to protect patient privacy

### Audit Trail
Every action is logged for compliance:
- **File uploads**: Timestamp, file size, processing time
- **AI analysis**: Confidence scores, risk assessments
- **Data access**: Download tracking, user interactions
- **Storage details**: S3 location, metadata preservation

##  Troubleshooting

- Ensure the file is a valid PDF
- Check file size (should be under 10MB)
- Normal processing time is 1-2 seconds

## Tech stack

**Backend:** AWS Lambda (Node.js) with three functions - PDF processing, data retrieval, and secure file access. OpenAI GPT-4 integration for AI analysis. S3 for file storage, DynamoDB for analysis results.

**Frontend:** React.js single-page app with hooks for state management. Real-time updates, responsive design, and graceful error handling.

**Security:** No sensitive data stored in browser - everything goes through HTTPS to the API. File uploads are validated client-side, but all real processing happens server-side. PHI detection happens before AI processing to protect privacy.

**Deployment:** AWS SAM for infrastructure-as-code, automated deployments via CloudFormation. Git version control with clean commit history and proper branching strategy.
