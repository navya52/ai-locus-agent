# How to Use Patient Context

A clinical letter processing system that helps doctors quickly understand patient history from PDF letters.

## Live Demo
### Step 1: Access the Application

1. Navigate to: http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com
2. You'll see the main interface with two tabs:
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

## Added some Interactive Features to visualize data treatment

### Security Compliance Badge
- **Look for** the "Security Compliance" badge (top right)
- **Hover over it** to see security features and compliance details

### Audit Trail
- **Go to** "📋 View Letters" tab
- **Hover over** "DATABASE AUDIT TRAIL ?" buttons
- **See** actual database records and file storage details
  
## Privacy Protection Demo

**Added a feature to filter out sensitive data before LLM calls**
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

## Error Handling & Graceful Degradation

If something goes wrong, you'll get friendly messages instead of scary error codes. For example:
- **PDF processing fails** → "Unable to read this file, please try a different PDF"
- **AI analysis times out** → "Analysis taking longer than expected, please wait"
- **Network issues** → "Connection problem, please check your internet and try again"

We also have fallbacks - if the AI can't analyze a document, we still extract the NHS number (using a regex algorithm) and store the file.

## Troubleshooting

- **File issues**: Ensure PDF is valid and under 10MB
- **Website access**: modile devices need to manually type "http://" before URL
- **Processing time**: Normal is 1-2 seconds

## Tech stack
<img width="1332" height="656" alt="Screenshot 2025-08-14 at 14 04 33" src="https://github.com/user-attachments/assets/2e4dbf69-99b4-4b1b-83e4-d23d07395d4f" />


**Backend:** AWS Lambda (Node.js) with three functions - PDF processing, data retrieval, and secure file access. OpenAI GPT-4 integration for AI analysis. S3 for file storage, DynamoDB for analysis results (product use case tradeoffs discussed below).

**Frontend:** React.js single-page app with hooks for state management. Real-time updates, responsive design, and graceful error handling.

**Security:** No sensitive data stored in browser - everything goes through HTTPS to the API. File uploads are validated client-side, but all real processing happens server-side. PHI detection happens before AI processing to protect privacy.


**Deployment:**  When we push code, it automatically builds and deploys to AWS. No manual server management needed, everything's serverless and scales automatically. AWS SAM for infrastructure-as-code, automated deployments via CloudFormation. Git version control with clean commit history and proper branching strategy.

**Data Storage Security & Future Scaling:**
Our current approach uses AWS DynamoDB with S3 for secure storage - Patient files are stored in secure digital vaults (like a locked filing cabinet) and the AI analysis is kept in an encrypted database (like a password-protected medical record) - only authorized staff can access either one.
In tech terms, PDFs go into private S3 buckets with unique keys, while analysis data gets AES-256 encrypted in DynamoDB with strict IAM access controls. 

For future scaling, for example when someone searches "find similar heart conditions":
we can consider a hybrid approach: keep DynamoDB for fast, cost-effective primary storage, but add an OpenSearch cluster for indexing. The tradeoff is complexity vs. functionality - OpenSearch is faster for indexing that DynamoDB, essentially because of the way it stores data. We can discuss this in depth if needed.


## System Logging & Debugging
In production it is important to monitor performance and resolve errors quickly. All our logs go to AWS CloudWatch, so if something breaks, we can quickly figure out what happened and fix it.
Everything gets logged for debugging and compliance. We track:
- **Errors**: What went wrong, when, and why
- **Security events**: PHI detection  (Access attempts,data access logs in the future)
- **User actions**: File uploads, downloads, analysis requests
- **System performance**: Processing times, API response times



