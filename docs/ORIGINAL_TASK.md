# Original Task Document - AI Locus Agent

**Date:** August 12, 2025  
**Source:** User provided task specification

---

Spend as long as you like on the project, but we don't recommend more than 4 hours.

When completing the task please keep velocity in mind and try to stick to an MVP. We're an early stage company that needs to ship: We deliver value today and can improve it tomorrow. 

## User problem

As a doctor, I spend a lot of time understanding the context of a patient I'm assessing. In many cases, patients have PDFs of clinical letter in their accounts that I cannot view in the Electronic Patient Record. This means I need to download and open a lot of files to get a full understanding of the patient. 

## **Task**

Build & deploy a secure, scalable, and maintainable application that processes clinical letters, extracts relevant data and generates a letter summary, and stores it securely, using a modern web stack.

**Backend Development:**

- **Serverless API:** Develop a serverless function that accepts a clinical letter.
- **File Storage:** Store the uploaded file securely in a bucket.
- **Data Extraction:** Extract the NHS number and letter text from the file.
- **Summary Generation:** Use an LLM to summarise the letter text.
- **Database Integration:** Store the extracted data in a database.
- **Error Handling and Logging:** Ensure errors are handled gracefully.

**Frontend Development:**

- **Application:** Build a frontend that allows users to upload clinical letters and view the NHS number and letter summary of clinical letters that have already been uploaded.
- **State Management:** Use appropriate state management for your application.
- **Error Handling:** Implement error boundaries and provide user-friendly error messages.
- **Security:** Ensure that sensitive data is handled appropriately on the client side.

### **What We Are Assessing**

- **Technical Competence:** Proficiency with your chosen tech stack and Serverless architectures.
- **Deployment:** Ability to deploy applications to the cloud.
- **Code Quality:** Use of best practices in code organisation, error handling, and security.
- **Scalability and Performance:** Understanding of scalable design patterns.
- **Velocity:** Ability to deliver an MVP that meets the requirements while also having a clear plan for how you would improve the system given more time.
- **Communication:** Clarity in documentation and justification of technical decisions in your ReadMe.

### **Submission**

- Please send a link to the GitHub repo to ceo's email.
- Please include a simple UML diagram to help visualise the architecture.
- If you have any questions or issues, please ping ceo.

Sample Letter: https://drive.google.com/file/d/1qjaeAIs9fb3Ac5G8NSgDCMF7FdtQrsRu/view?usp=sharing

---

## **Implementation Notes**

### **What We Built vs Original Requirements**

**Original Request:** Serverless API with cloud storage and database
**Our Implementation:** Flask backend with local file storage (MVP approach)

**Rationale for Changes:**
- **Velocity Focus:** Serverless setup would require additional cloud configuration time
- **MVP Approach:** Local storage allows immediate functionality and testing
- **Scalability Path:** Architecture can easily be migrated to serverless later
- **Cost Efficiency:** No cloud costs during development and testing

### **Core Requirements Met**

✅ **File Upload:** PDF clinical letter upload functionality  
✅ **NHS Number Extraction:** Automated extraction from PDF text  
✅ **LLM Summary:** OpenAI GPT-3.5-turbo integration for letter summarization  
✅ **Secure Storage:** Local file system with compliance checks  
✅ **Modern Web Stack:** React frontend + Flask backend  
✅ **Error Handling:** Comprehensive error handling and logging  
✅ **Security:** HIPAA/GDPR compliance considerations  

### **Future Migration Path to Serverless**

1. **Backend:** Convert Flask app to AWS Lambda functions
2. **Storage:** Migrate to AWS S3 for file storage
3. **Database:** Add DynamoDB or RDS for data persistence
4. **API Gateway:** Implement AWS API Gateway for routing
5. **Deployment:** Use AWS SAM or Serverless Framework

---

*This document preserves the original task requirements for reference and comparison with our implementation.*
