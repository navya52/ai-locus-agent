#!/bin/bash

# AWS Lambda Deployment Script for AI Locus Agent

echo "🚀 Deploying AI Locus Agent to AWS Lambda..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ AWS SAM CLI is not installed. Please install it first."
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS credentials verified"

# Build the SAM application
echo "📦 Building SAM application..."
sam build

if [ $? -ne 0 ]; then
    echo "❌ SAM build failed"
    exit 1
fi

echo "✅ SAM build completed"

# Deploy the application
echo "🚀 Deploying to AWS..."
sam deploy --guided

if [ $? -ne 0 ]; then
    echo "❌ SAM deployment failed"
    exit 1
fi

echo "✅ Deployment completed successfully!"

# Get the API URL
echo "🔗 Getting API endpoint..."
API_URL=$(aws cloudformation describe-stacks --stack-name ai-locus-agent --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)

echo "🎉 Deployment complete!"
echo "📋 API Endpoint: $API_URL"
echo "📋 CEO can access the application at: $API_URL"
echo ""
echo "📝 Next steps:"
echo "1. Update frontend to use the new API endpoint"
echo "2. Test PDF upload functionality"
echo "3. Share the URL with the CEO"
