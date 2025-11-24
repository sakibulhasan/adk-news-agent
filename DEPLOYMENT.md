# Vertex AI Agent Engine CI/CD Deployment Guide

This guide explains how to set up continuous integration and deployment (CI/CD) for the News Agent application to Google Cloud Vertex AI Agent Engine.

## Prerequisites

1. **Google Cloud Platform Account**
   - Active GCP account with billing enabled
   - A GCP project created with Vertex AI API enabled

2. **GitHub Repository**
   - Code pushed to a GitHub repository
   - Admin access to repository settings

3. **Required Tools** (for local setup)
   - Google Cloud CLI (`gcloud`)
   - Python 3.8+
   - Google ADK (`pip install google-adk`)

## Quick Setup

### 1. Run the Setup Script

```bash
./scripts/setup-gcp.sh
```

This script will:
- Enable required Vertex AI APIs
- Create service accounts with proper permissions
- Generate service account keys
- Configure Vertex AI Agent Engine access

### 2. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `GCP_PROJECT_ID`: Your Google Cloud Project ID
- `GOOGLE_API_KEY`: Your Gemini API key
- `GCP_SERVICE_ACCOUNT_KEY`: Content of the generated `key.json` file

### 3. Deploy

Push your code to the `main` branch, and the deployment will start automatically!

## Manual Setup (Alternative)

If you prefer to set up manually, follow these steps:

### 1. Enable GCP APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com 
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 2. Create Service Account

```bash
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 3. Create Service Account Key

```bash
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 4. Store API Key in Secret Manager

```bash
echo -n "YOUR_GOOGLE_API_KEY" | gcloud secrets create google-api-key --data-file=-
```

## Architecture Overview

### CI/CD Pipeline Components

1. **GitHub Actions Workflow** (`.github/workflows/deploy.yml`)
   - Triggers on push to main branch
   - Runs tests
   - Builds Docker image
   - Pushes to Google Container Registry
   - Deploys to Cloud Run

2. **Docker Container** (`Dockerfile`)
   - Python 3.11 slim base image
   - FastAPI web server
   - Optimized for Cloud Run

3. **FastAPI Application** (`main.py`)
   - RESTful API endpoints
   - Health checks for load balancer
   - Integration with your news agent

4. **Google Cloud Run**
   - Serverless container platform
   - Auto-scaling (0-10 instances)
   - Pay-per-request pricing

### Agent Interaction

Once deployed, your agent will be available through:

- **Vertex AI Console**: https://console.cloud.google.com/ai/agents
- **Agent Builder**: For integration with other applications
- **API Access**: Through Vertex AI Agent Engine API
- **Chat Interface**: Direct conversation with the agent

### Example Usage

```bash
# Access through gcloud CLI
gcloud ai agents list --region=us-central1

# Interact with agent via API (example)
curl -X POST "https://aiplatform.googleapis.com/v1/projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID:predict" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the top 5 news stories in London today?"}'
```

### Local Testing

You can also deploy and test locally:

```bash
# Run local deployment script
python scripts/deploy-local.py

# Or manually with ADK
adk deploy --agent-config agent_config.yaml --source-path .
```

## Configuration

### Environment Variables

The application uses these environment variables:

- `GOOGLE_API_KEY`: Your Gemini API key (stored in Secret Manager)
- `PORT`: Port number (automatically set by Cloud Run)

### Resource Limits

Current configuration:
- Memory: 1GB
- CPU: 1 vCPU
- Timeout: 300 seconds
- Concurrency: 80 requests per instance
- Min instances: 0 (scales to zero)
- Max instances: 10

## Monitoring and Logs

### View Logs
```bash
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=news-agent-api" --limit 50
```

### Monitor Service
```bash
gcloud run services describe news-agent-api --region=us-central1
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Verify Docker syntax in `Dockerfile`

2. **Deployment Failures**
   - Ensure service account has proper permissions
   - Check that API key is correctly stored in Secret Manager

3. **Runtime Errors**
   - Check Cloud Run logs for Python errors
   - Verify that `google-adk` is compatible with the container environment

### Debug Commands

```bash
# Check service status
gcloud run services list

# View service details
gcloud run services describe news-agent-api --region=us-central1

# Check recent logs
gcloud logs tail "resource.type=cloud_run_revision" --filter="resource.labels.service_name=news-agent-api"
```

## Security Best Practices

1. **API Keys**: Stored in Google Secret Manager, not in code
2. **Service Account**: Minimal required permissions
3. **Network**: HTTPS only, with Cloud Run's built-in security
4. **Container**: Non-root user, minimal attack surface

## Cost Optimization

- **Scaling**: Configured to scale to zero when not in use
- **Resources**: Right-sized for typical workloads
- **Pricing**: Pay only for actual requests and compute time

## Next Steps

1. **Custom Domain**: Configure a custom domain for your service
2. **Authentication**: Add API key authentication if needed
3. **Rate Limiting**: Implement rate limiting for production use
4. **Monitoring**: Set up alerting and monitoring dashboards
5. **Database**: Add persistent storage if needed

For more information, see the [Google Cloud Run documentation](https://cloud.google.com/run/docs).