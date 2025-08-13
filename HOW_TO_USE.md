# How to Use AI Locus Agent

A comprehensive guide to using the AI Locus Agent system for clinical letter processing and analysis.

## 🚀 Live Demo

**Access the application**: http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com

## 📋 Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- PDF clinical letters to upload
- Internet connection

## 🎯 Getting Started

### Step 1: Access the Application
1. Open your web browser
2. Navigate to: http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com
3. You'll see the main interface with two tabs:
   - **📄 Upload Letter** - For processing new letters
   - **📋 View Letters** - For viewing previously processed letters

### Step 2: Upload Your First Letter
1. Click on the **"📄 Upload Letter"** tab
2. Click **"Choose File"** or drag and drop a PDF clinical letter
3. Click **"Upload and Analyze"**
4. Wait for processing (typically 1-2 seconds)
5. View the results showing:
   - NHS number extraction
   - AI-generated summary
   - Risk assessment
   - Key findings and recommendations

## 🔍 Testing the Interactive Features

### Testing GDPR Compliance Hover Tooltip
1. **Upload a letter** and wait for processing
2. **Switch to "📋 View Letters"** tab
3. **Look for the "GDPR COMPLIANT"** badge (green button with checkmark)
4. **Hover over the badge** - a detailed tooltip will appear showing:
   - Data Minimization principles
   - Right to Erasure implementation
   - Data Portability features
   - Consent Management details
   - Audit Trail capabilities
   - Encryption standards
   - Data Retention policies

### Testing Database Audit Trail Hover Tooltip
1. **In the "📋 View Letters"** tab
2. **Look for "DATABASE AUDIT TRAIL ?"** button (next to letter date)
3. **Hover over the button** - a tooltip will appear showing:
   - **Title**: "DynamoDB Record Details"
   - **JSON blob** with actual database record structure:
     ```json
     {
       "storage_id": "storage_1755049123456_abc123def",
       "file_storage": {
         "success": true,
         "s3_key": "uploads/storage_1755049123456_abc123def/filename.pdf",
         "file_size": 12345,
         "upload_timestamp": "2025-08-13T02:38:51.123Z"
       },
       "processing_time": 1.2,
       "nhs_number": "7052493519",
       "ai_confidence": 85
     }
     ```

## 📊 Understanding the Results

### Upload Results Display
After uploading a letter, you'll see:

**Letter Information:**
- **Filename**: Original PDF name
- **Word Count**: Number of words extracted
- **Character Count**: Total characters
- **NHS Number**: Extracted NHS identifier
- **Text Preview**: First 200 characters of the letter

**AI Analysis:**
- **AI Summary**: Comprehensive summary of the letter content
- **Risk Level**: Low/Medium/High classification
- **Confidence**: AI confidence score (0-100%)
- **Key Findings**: Important clinical points
- **Urgent Concerns**: Critical issues identified
- **Risk Factors**: Potential risk indicators
- **Recommended Actions**: Suggested next steps

**Processing Information:**
- **Processing Time**: How long the analysis took
- **Storage ID**: Unique identifier for the record

### View Letters Display
In the "View Letters" tab, each letter shows:

**Letter Card:**
- **Date and Time**: When the letter was processed
- **NHS Number**: Extracted identifier
- **Urgency Level**: Risk classification
- **Risk Factors**: Number of identified risks
- **Key Findings**: Number of findings
- **AI Confidence**: Confidence percentage
- **Processing Date**: Formatted date
- **Risk Bar**: Visual representation of risk level
- **Download Button**: Access to original PDF (if available)

## 🔧 Advanced Features

### Downloading Original PDFs
1. **In "View Letters"** tab, look for **"📄 Download Original PDF"** button
2. **Click the button** - a secure download link will be generated
3. **The file will download** with the original filename
4. **Note**: Downloads are tracked for audit purposes

### Understanding Risk Levels
- **🟢 Low Risk**: Routine appointments, standard care
- **🟡 Medium Risk**: Requires attention, follow-up needed
- **🔴 High Risk**: Urgent care required, immediate action

### AI Confidence Scores
- **90-100%**: High confidence in analysis
- **70-89%**: Good confidence with minor uncertainties
- **50-69%**: Moderate confidence, review recommended
- **Below 50%**: Low confidence, manual review advised

## 🛡️ Security and Compliance Features

### GDPR Compliance
The system implements comprehensive GDPR compliance:
- **Data Minimization**: Only processes necessary information
- **Right to Erasure**: Complete data deletion capability
- **Data Portability**: Export functionality available
- **Consent Management**: Clear consent tracking
- **Audit Trails**: Complete access logging
- **Encryption**: Data encrypted in transit and at rest
- **Data Retention**: Automatic cleanup policies

### Audit Trail
Every action is logged for compliance:
- **File uploads**: Timestamp, file size, processing time
- **AI analysis**: Confidence scores, risk assessments
- **Data access**: Download tracking, user interactions
- **Storage details**: S3 location, metadata preservation

## 🚨 Troubleshooting

### Common Issues

**File Upload Fails:**
- Ensure the file is a valid PDF
- Check file size (should be under 10MB)
- Verify internet connection

**No NHS Number Found:**
- The letter might not contain a valid NHS number
- Check if the number format is standard (10 digits)
- Some letters may use different identifier formats

**Low AI Confidence:**
- The letter content might be unclear or incomplete
- Try uploading a different letter
- Check if the text is properly extracted

**Processing Takes Too Long:**
- Normal processing time is 1-2 seconds
- If longer, check your internet connection
- The system will timeout after 30 seconds

### Browser Compatibility
- **Chrome**: Full support (recommended)
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support
- **Internet Explorer**: Not supported

## 📞 Support

If you encounter issues:
1. **Check the troubleshooting section** above
2. **Try refreshing the page**
3. **Clear browser cache** and try again
4. **Contact support** with specific error details

## 🔄 System Updates

The system is continuously updated with:
- **Performance improvements**
- **New AI capabilities**
- **Enhanced security features**
- **Better user experience**

Check the application regularly for the latest features and improvements.

---

**Built for healthcare professionals with security and compliance in mind**
