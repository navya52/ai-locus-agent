# How to Use Patient Context

A clinical letter processing system that helps doctors quickly understand patient history from PDF letters.

## Live Demo

1. Navigate to http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com

## Getting Started

### Step 1: Access the Application
2. Navigate to: http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com
 (Only HTTP works for now, had to rollback HTTPS last minute due to CloudFront's free plan not being suitable)
3. You'll see the main interface with two tabs:
   - **Upload Letter** - For processing new letters
   - **View Letters** - For viewing previously processed letters (letters already exist from me testing)

### Step 2: Process Your First Letter
1. Click **"📄 Upload Letter"**
2. Upload a PDF clinical letter (drag & drop or click to select)
3. Click **"Upload and Analyze"**
4. Wait 1-2 seconds for processing
5. Review the results:
   - **NHS number** (automatically extracted)
   - **AI summary** (key clinical points)
   - **Risk assessment** (urgency level)
   - **Key findings** (important details)

## Interactive Features

### Security Compliance Badge
- **Look for** the "Security Compliance" badge (top right)
- **Hover over it** to see security features and compliance details

### Audit Trail
- **Go to** "📋 View Letters" tab
- **Hover over** "DATABASE AUDIT TRAIL ?" buttons
- **See** actual database records and file storage details
  
## Privacy Protection Demo

**Test PHI Detection:**
1. Upload "Sample_File_with_PHI.pdf" from the project root
2. **Watch** the privacy protection dialog appear
3. **See** how patient names are automatically detected and masked
4. **Note** that NHS numbers are preserved for clinical continuity

### Audit Trail
Every action is logged for compliance:
- **File uploads**: Timestamp, file size, processing time
- **AI analysis**: Confidence scores, risk assessments
- **Data access**: Download tracking, user interactions
- **Storage details**: S3 location, metadata preservation

## Real-World Use Cases

**For Doctors:**
- Quickly understand patient history from multiple letters
- Identify urgent cases that need immediate attention
- Access patient information without opening multiple PDFs
- Maintain audit trails for compliance

**For Healthcare Teams:**
- Share patient summaries with colleagues
- Track patient progress over time
- Ensure privacy compliance with automatic PHI detection
- Access original documents when needed

## Error Handling & Graceful Degradation

If something goes wrong, you'll get friendly messages instead of scary error codes. For example:
- **PDF processing fails?** → "Unable to read this file, please try a different PDF"
- **AI analysis times out?** → "Analysis taking longer than expected, please wait"
- **Network issues?** → "Connection problem, please check your internet and try again"

We also have fallbacks - if the AI can't analyze a document, we still extract the NHS number (using regex algorithm) and store the file.

## Troubleshooting

**For Doctors:**
- Quickly understand patient history from multiple letters
- Identify urgent cases that need immediate attention
- Access patient information without opening multiple PDFs
- Maintain audit trails for compliance

**For Healthcare Teams:**
- Share patient summaries with colleagues
- Track patient progress over time
- Ensure privacy compliance with automatic PHI detection
- Access original documents when needed

## Troubleshooting

- **File issues**: Ensure PDF is valid and under 10MB
- **Mobile access**: May need to manually type "http://" before URL
- **Processing time**: Normal is 1-2 seconds

## Tech stack
<img width="1157" height="600" alt="Screenshot 2025-08-13 at 06 11 37" src="https://github.com/user-attachments/assets/91f1328f-e5a4-4f12-995c-a4dee1120745" />

**Backend:** AWS Lambda (Node.js) with three functions - PDF processing, data retrieval, and secure file access. OpenAI GPT-4 integration for AI analysis. S3 for file storage, DynamoDB for analysis results (product use case tradeoffs discussed below).

**Frontend:** React.js single-page app with hooks for state management. Real-time updates, responsive design, and graceful error handling.

**Security:** No sensitive data stored in browser - everything goes through HTTPS to the API. File uploads are validated client-side, but all real processing happens server-side. PHI detection happens before AI processing to protect privacy.


**Deployment:**  When we push code, it automatically builds and deploys to AWS. No manual server management needed, everything's serverless and scales automatically. AWS SAM for infrastructure-as-code, automated deployments via CloudFormation. Git version control with clean commit history and proper branching strategy.

**Data Storage Security & Future Scaling:**
Our current approach uses AWS DynamoDB with S3 for secure storage - Patient files are stored in secure digital vaults (like a locked filing cabinet) and the AI analysis is kept in an encrypted database (like a password-protected medical record) - only authorized staff can access either one.
In tech terms, PDFs go into private S3 buckets with unique keys, while analysis data gets AES-256 encrypted in DynamoDB with strict IAM access controls. 

For future scaling, for example when someone searches "find similar heart conditions":
we're considering a hybrid approach: keep DynamoDB for fast, cost-effective primary storage, but add an OpenSearch cluster . The tradeoff is complexity vs. functionality - OpenSearch is faster for indexing that DynamoDB, essentially because of the way it stores data. We can discuss this in depth if needed.


## System Logging & Debugging
In production it is important to monitor problems and resolve them quickly. All our logs go to AWS CloudWatch, so if something breaks, we can quickly figure out what happened and fix it.
Everything gets logged for debugging and compliance. We track:
- **Errors**: What went wrong, when, and why
- **Security events**: PHI detection  (Access attempts,data access logs are one step away)
- **User actions**: File uploads, downloads, analysis requests
- **System performance**: Processing times, API response times



