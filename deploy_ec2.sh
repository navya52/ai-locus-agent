#!/bin/bash

# Full-Stack EC2 Deployment Script for AI Locus Agent

echo "🚀 Deploying AI Locus Agent to EC2..."

# Configuration
EC2_IP="3.8.125.120"
EC2_USER="ec2-user"
PROJECT_DIR="/home/ec2-user/ai-locus-agent"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}✅ EC2 Instance: ${EC2_IP}${NC}"

# Step 1: Build React frontend
echo -e "${YELLOW}📦 Building React frontend...${NC}"
cd frontend
npm run build
cd ..

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ React build failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ React build completed${NC}"

# Step 2: Create deployment package
echo -e "${YELLOW}📦 Creating deployment package...${NC}"
tar -czf deployment.tar.gz \
    server.js \
    package.json \
    frontend/build/ \
    lambda_functions/ \
    --exclude=node_modules \
    --exclude=.git

echo -e "${GREEN}✅ Deployment package created${NC}"

# Step 3: Upload to EC2
echo -e "${YELLOW}📤 Uploading to EC2...${NC}"
scp -i ~/.ssh/ai-locus-key.pem deployment.tar.gz ${EC2_USER}@${EC2_IP}:~/

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Upload failed. Make sure you have the SSH key: ~/.ssh/ai-locus-key.pem${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Upload completed${NC}"

# Step 4: Deploy on EC2
echo -e "${YELLOW}🚀 Deploying on EC2...${NC}"
ssh -i ~/.ssh/ai-locus-key.pem ${EC2_USER}@${EC2_IP} << 'EOF'
    # Stop existing process
    pm2 stop ai-locus-agent || true
    pm2 delete ai-locus-agent || true
    
    # Create project directory
    mkdir -p /home/ec2-user/ai-locus-agent
    cd /home/ec2-user/ai-locus-agent
    
    # Extract deployment package
    tar -xzf ~/deployment.tar.gz
    rm ~/deployment.tar.gz
    
    # Install dependencies
    npm install
    
    # Start the application
    pm2 start server.js --name "ai-locus-agent"
    pm2 save
    pm2 startup
    
    echo "✅ Deployment completed!"
    echo "🌐 Your app is available at: http://3.8.125.120:3000"
    echo "🔗 Health check: http://3.8.125.120:3000/api/health"
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}🎉 Deployment successful!${NC}"
    echo -e "${GREEN}🌐 Your full-stack app is now running at: http://3.8.125.120:3000${NC}"
    echo -e "${GREEN}🔗 Health check: http://3.8.125.120:3000/api/health${NC}"
else
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi

# Cleanup
rm deployment.tar.gz

echo -e "${GREEN}✅ Deployment complete!${NC}"
