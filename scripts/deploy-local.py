#!/usr/bin/env python3
"""
Local deployment script for Vertex AI Agent Engine
Use this to deploy your agent manually or test the deployment locally
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        sys.exit(1)

def main():
    # Check if we're in the right directory
    if not Path("news_agent").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Get environment variables
    project_id = os.getenv('GCP_PROJECT_ID') or input("Enter your GCP Project ID: ")
    region = os.getenv('REGION', 'us-central1')
    google_api_key = os.getenv('GOOGLE_API_KEY') or input("Enter your Google API Key: ")
    
    print(f"🚀 Deploying News Agent to Vertex AI Agent Engine")
    print(f"Project: {project_id}")
    print(f"Region: {region}")
    print("=" * 50)
    
    # Ensure we're authenticated
    run_command("gcloud auth application-default login --no-launch-browser", "Authenticating with GCP")
    
    # Set the project
    run_command(f"gcloud config set project {project_id}", "Setting GCP project")
    
    # Enable required APIs
    apis = [
        "aiplatform.googleapis.com",
        "discoveryengine.googleapis.com",
        "dialogflow.googleapis.com"
    ]
    
    for api in apis:
        run_command(f"gcloud services enable {api}", f"Enabling {api}")
    
    # Install ADK if not already installed
    try:
        subprocess.run(["adk", "--version"], check=True, capture_output=True)
        print("✅ ADK CLI already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        run_command("pip install google-adk", "Installing Google ADK")
    
    # Create agent config with environment variables
    config_content = f"""
name: news-agent
description: "Multi-agent news retrieval system built with Google's Agent Development Kit (ADK)"
model: "gemini-2.5-flash"
display_name: "News Agent"
instructions: |
  You are a professional News Curator that finds the top 10 most current and relevant news headlines 
  for the city or country provided by the user.

  Execution Steps:
  1. Identify the location from the user's query.
  2. Use the SearchSpecialist agent to execute Google Search queries for current news.
  3. Synthesize the raw search results into a clear, concise, and numbered list of the top 10 headlines.
  4. For EACH headline, include the date of occurrence if available. Format: "[Date] - Headline text".
  5. If a date is not available, indicate it as "[Date unknown] - Headline text".
  6. Only respond with the synthesized news report.
  7. If no location is provided, politely ask the user for one.

tools:
  - name: google_search
    description: "Search for current news and information using Google Search"

agents:
  - name: SearchSpecialist
    description: "A specialist agent that executes Google Search queries for current events"
    model: "gemini-2.5-flash"
    instructions: |
      You are a specialist in using Google Search to find current, trending information.
      When asked for news about an area, use the 'google_search' tool precisely.
      Formulate search queries like: 'top 10 news headlines for [Location] today'.
      Return raw search results with any available date information for processing.
    tools:
      - name: google_search

environment_variables:
  GOOGLE_API_KEY: "{google_api_key}"
  GOOGLE_GENAI_USE_VERTEXAI: "0"

deployment:
  region: "{region}"
  project_id: "{project_id}"
"""
    
    with open("agent_config_local.yaml", "w") as f:
        f.write(config_content)
    
    print("✅ Created local agent configuration")
    
    # Deploy the agent
    deploy_command = f"""
    adk deploy \
      --project {project_id} \
      --region {region} \
      --agent-config agent_config_local.yaml \
      --source-path . \
      --agent-name news-agent
    """
    
    run_command(deploy_command, "Deploying agent to Vertex AI Agent Engine")
    
    # Get agent details
    try:
        agent_list = run_command(
            f"gcloud ai agents list --region={region} --format=json",
            "Getting agent details"
        )
        agents = json.loads(agent_list)
        news_agents = [a for a in agents if 'news-agent' in a.get('displayName', '').lower()]
        
        if news_agents:
            agent_id = news_agents[0]['name']
            print(f"🎉 Agent deployed successfully!")
            print(f"📍 Agent ID: {agent_id}")
            print(f"🌐 Access your agent at: https://console.cloud.google.com/ai/agents?project={project_id}")
        else:
            print("⚠️  Agent deployed but couldn't retrieve details. Check the console.")
            
    except Exception as e:
        print(f"⚠️  Agent deployed but couldn't retrieve details: {e}")
        print(f"🌐 Check your agent at: https://console.cloud.google.com/ai/agents?project={project_id}")
    
    # Cleanup
    if Path("agent_config_local.yaml").exists():
        os.remove("agent_config_local.yaml")
        print("🧹 Cleaned up temporary files")
    
    print("\n🎊 Deployment completed successfully!")
    print("You can now test your agent in the Vertex AI Console.")

if __name__ == "__main__":
    main()