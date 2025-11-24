# Vertex AI Agent Engine Deployment

## Overview

Your News Agent is now configured to deploy to **Vertex AI Agent Engine** instead of Cloud Run. This provides a more native agent experience with Google's AI platform.

## Key Changes Made

### 1. **Updated CI/CD Pipeline** (`.github/workflows/deploy.yml`)
- Removed Docker containerization
- Added ADK CLI installation
- Changed deployment target to Vertex AI Agent Engine
- Updated required GCP APIs and permissions

### 2. **Agent Configuration** (`agent_config.yaml`)
- Defined agent behavior and instructions
- Configured multi-agent architecture
- Set up environment variables
- Specified deployment parameters

### 3. **Updated Setup Script** (`scripts/setup-gcp.sh`)
- Enables Vertex AI APIs instead of Cloud Run APIs
- Grants appropriate Vertex AI permissions
- Configures service account for agent deployment

### 4. **Local Deployment Script** (`scripts/deploy-local.py`)
- Allows manual deployment for testing
- Handles authentication and configuration
- Provides deployment status and access information

## Deployment Options

### Option 1: Automated CI/CD (Recommended)
1. Run setup script: `./scripts/setup-gcp.sh`
2. Configure GitHub secrets
3. Push to main branch

### Option 2: Manual Local Deployment
```bash
python scripts/deploy-local.py
```

### Option 3: Direct ADK CLI
```bash
adk deploy --agent-config agent_config.yaml --source-path .
```

## Benefits of Vertex AI Agent Engine

✅ **Native Agent Platform**: Purpose-built for AI agents
✅ **Managed Infrastructure**: No container management needed
✅ **Integrated Tools**: Built-in support for Google Search and other tools
✅ **Conversational Interface**: Natural chat-based interactions
✅ **Enterprise Ready**: Built-in security and compliance features
✅ **Cost Effective**: Pay only for agent interactions

## Access Your Deployed Agent

Once deployed, access your agent at:
- **Console**: https://console.cloud.google.com/ai/agents
- **API**: Via Vertex AI Agent Engine API
- **Integrations**: Through Agent Builder

Your agent will be able to:
- Accept natural language queries about news
- Search for current news using Google Search
- Format results into readable news reports
- Handle multiple locations and date-specific requests

The multi-agent architecture ensures specialized search capabilities while maintaining a user-friendly interface for news curation.