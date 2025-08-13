# How to Use AI Patient Context SUmmary Generator

## Live Demo

1. Navigate to http://ai-locus-agent-frontend.s3-website.eu-west-2.amazonaws.com

2. You'll see the main interface with two tabs:
   - **Upload Letter** - For processing new letters
   - **View Letters** - For viewing previously processed letters (letters might already exist from testing)

### Upload Your First Letter
1. Click on the **" Upload Letter"** tab
2. Click **"Choose File"** or drag and drop a PDF clinical letter
3. Click **"Upload and Analyze"**
4. Wait for processing (typically 1-2 seconds)
5. View the results showing:
   - NHS number extraction
   - AI-generated summary
   - Risk assessment
   - Key findings and recommendations

### Try the Security Compliance Hover Tooltip on the top right corner
1. **Look for the "Security COmpliance"** badge in the top right, a detailed tooltip will appear showing cool stuff

### Try the Database Audit Trail Hover Tooltip
1. **In the " View Letters"** tab
2. **Look for "DATABASE AUDIT TRAIL ?"** button (next to letter date)
3. **Hover over the button** - a tooltip will appear showing details of the data base storage. Security concerns in DB are addressed later in this doc.
  
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

## Error Handling & Graceful Degradation

 If something goes wrong, you'll get friendly messages instead of scary error codes. For example:
- **PDF processing fails?** → "Unable to read this file, please try a different PDF"
- **AI analysis times out?** → "Analysis taking longer than expected, please wait"
- **Network issues?** → "Connection problem, please check your internet and try again"

We also have fallbacks - if the AI can't analyze a document, we still extract the NHS number (using regex algorithm) and store the file.

##  Troubleshooting

- Ensure the file is a valid PDF
- Check file size (should be under 10MB)
- Mobile devices might need a manual http address input
- Normal processing time is 1-2 seconds

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



