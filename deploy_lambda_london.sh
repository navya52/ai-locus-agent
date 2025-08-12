#!/bin/bash

# London Lambda Deployment Script for AI Locus Agent

echo "🚀 Deploying AI Locus Agent to London Lambda function..."

# Configuration
FUNCTION_NAME="ai-locus-agent-upload-london"
REGION="eu-west-2"
LAMBDA_DIR="lambda_functions"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS credentials verified"

# Create deployment package
echo "📦 Creating deployment package..."
cd $LAMBDA_DIR

# Create a temporary directory for the package
TEMP_DIR=$(mktemp -d)
cp upload_letter.py $TEMP_DIR/

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt -t $TEMP_DIR/ 2>/dev/null || echo "⚠️  Dependencies not installed (pip3 not available)"
fi

# Create zip file
cd $TEMP_DIR
zip -r ../lambda_deployment_london.zip .
cd ..

echo "✅ Deployment package created"

# Update Lambda function
echo "🚀 Updating London Lambda function..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://lambda_deployment_london.zip \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ London Lambda function updated successfully!"
    
    # Get the function URL
    echo "🔗 Getting function URL..."
    FUNCTION_URL=$(aws lambda get-function-url-config \
        --function-name $FUNCTION_NAME \
        --region $REGION \
        --query 'FunctionUrl' \
        --output text 2>/dev/null)
    
    if [ -n "$FUNCTION_URL" ]; then
        echo "📋 Function URL: $FUNCTION_URL"
    else
        echo "📋 Function updated. You may need to configure API Gateway trigger."
    fi
    
else
    echo "❌ Failed to update London Lambda function"
    exit 1
fi

# Cleanup
rm -rf $TEMP_DIR
rm lambda_deployment_london.zip

echo "🎉 London deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Test the function in AWS Console (London region)"
echo "2. Configure API Gateway trigger if needed"
echo "3. Test with your frontend"
