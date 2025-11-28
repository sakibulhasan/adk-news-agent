#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Cloud Run CI/CD Pipeline for News Agent${NC}"
echo "========================================================="

# Check if required tools are installed
command -v gcloud >/dev/null 2>&1 || { echo -e "${RED}❌ Google Cloud CLI is not installed. Please install it first.${NC}" >&2; exit 1; }
command -v git >/dev/null 2>&1 || { echo -e "${RED}❌ Git is not installed. Please install it first.${NC}" >&2; exit 1; }

# Get project information
read -p "Enter your GCP Project ID: " PROJECT_ID
read -p "Enter your preferred region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

read -p "Enter your Google API Key: " GOOGLE_API_KEY

echo -e "${YELLOW}📋 Configuration Summary:${NC}"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "API Key: ${GOOGLE_API_KEY:0:10}..."

read -p "Continue with this configuration? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Setup cancelled${NC}"
    exit 1
fi

echo -e "${BLUE}🔧 Setting up GCP project for Cloud Run deployment...${NC}"

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs for Cloud Run
echo -e "${YELLOW}📡 Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Create service account for deployment
echo -e "${YELLOW}👤 Creating service account...${NC}"
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions Service Account" \
    --description="Service account for GitHub Actions CI/CD with Vertex AI"

# Grant necessary roles to the service account for Cloud Run
echo -e "${YELLOW}🔐 Granting Cloud Run permissions...${NC}"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

# Create and download service account key
echo -e "${YELLOW}🔑 Creating service account key...${NC}"
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com

echo -e "${GREEN}✅ GCP setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Go to your GitHub repository settings"
echo "2. Navigate to Settings > Secrets and variables > Actions"
echo "3. Add the following secrets:"
echo "   - GCP_PROJECT_ID: $PROJECT_ID"
echo "   - GOOGLE_API_KEY: $GOOGLE_API_KEY"
echo "   - GCP_SERVICE_ACCOUNT_KEY: (paste the content of key.json file)"
echo ""
echo "4. The service account key has been saved as 'key.json'"
echo "   Copy its content and add it as GCP_SERVICE_ACCOUNT_KEY secret"
echo ""
echo "5. Commit and push your code to trigger the deployment!"
echo ""
echo "6. After deployment, access your agent at the Cloud Run URL"
echo ""
echo -e "${YELLOW}⚠️  Important: Delete the key.json file after adding it to GitHub secrets${NC}"
echo -e "${GREEN}🎉 Your Cloud Run CI/CD pipeline is ready!${NC}"