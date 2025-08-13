# 🚀 AI Locus Agent - Vercel Deployment Guide

## Overview

This guide will help you deploy the AI Locus Agent to Vercel as a serverless application. The deployment will provide a live demo URL that can be shared without any local setup required.

## Prerequisites

1. **GitHub Account** - For hosting the repository
2. **Vercel Account** - For serverless deployment
3. **OpenAI API Key** - For AI processing

## Deployment Steps

### 1. Prepare the Repository

Ensure your repository structure looks like this:
```
ai-locus-agent/
├── frontend/          # React application
├── api/              # Vercel serverless functions
├── vercel.json       # Vercel configuration
└── README.md
```

### 2. Set Up Environment Variables

In your Vercel dashboard, add these environment variables:

```bash
OPENAI_API_KEY=your_openai_api_key_here
API_VERSION=1.0.0
MAX_PATIENT_DATA_LENGTH=10000
```

### 3. Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure the following settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (root of project)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/build`

#### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts to configure deployment
```

### 4. Configure Custom Domain (Optional)

1. In Vercel dashboard, go to your project
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

## Post-Deployment

### 1. Test the Deployment

Visit your Vercel URL and test:
- ✅ File upload functionality
- ✅ PDF processing
- ✅ AI analysis
- ✅ Results display

### 2. Share the Demo

Your live demo URL will be:
```
https://your-project-name.vercel.app
```

## Architecture

```
Frontend (React) → Vercel Edge Network → Serverless Functions → OpenAI API
```

### Serverless Functions

- **`/api/health`** - Health check endpoint
- **`/api/upload-letter`** - PDF processing and AI analysis
- **`/api/storage/*`** - Data storage operations

## Monitoring

### Vercel Analytics

- Function execution times
- Error rates
- Request volumes
- Performance metrics

### Logs

Access function logs in Vercel dashboard:
1. Go to your project
2. Click "Functions" tab
3. Select function to view logs

## Troubleshooting

### Common Issues

1. **Function Timeout**
   - Increase `maxDuration` in `vercel.json`
   - Optimize function performance

2. **Environment Variables**
   - Ensure all required variables are set
   - Check variable names match code

3. **CORS Issues**
   - Verify CORS headers in functions
   - Check frontend API calls

4. **File Upload Issues**
   - Check function payload limits
   - Verify multipart form handling

### Performance Optimization

1. **Cold Starts**
   - Use Vercel's edge functions where possible
   - Optimize function size

2. **Memory Usage**
   - Monitor function memory consumption
   - Optimize large file processing

## Cost Considerations

### Vercel Pricing (Free Tier)

- **Function Execution**: 100GB-hours/month
- **Bandwidth**: 100GB/month
- **Build Minutes**: 6000 minutes/month

### OpenAI Costs

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Typical Analysis**: ~700 tokens per PDF
- **Cost per Analysis**: ~$0.0014

## Security

### Environment Variables

- Never commit API keys to repository
- Use Vercel's environment variable system
- Rotate keys regularly

### CORS Configuration

- Restrict origins in production
- Use proper CORS headers
- Validate file uploads

## Next Steps

### Production Enhancements

1. **Database Integration**
   - Add DynamoDB for persistent storage
   - Implement user authentication

2. **File Storage**
   - Migrate to AWS S3
   - Implement file versioning

3. **Monitoring**
   - Add error tracking (Sentry)
   - Implement health checks

4. **Security**
   - Add rate limiting
   - Implement API authentication

---

## Support

For deployment issues:
1. Check Vercel documentation
2. Review function logs
3. Test locally with Vercel CLI
4. Contact support if needed

---

*Deployment completed successfully! Your AI Locus Agent is now live and ready for demos.*
