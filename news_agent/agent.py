# from google.adk.agents.llm_agent import Agent

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )

import os
import sys
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.sessions import Session

# --- 1. Environment Setup ---
# Load environment variables (like GOOGLE_API_KEY) from the .env file
load_dotenv()

# --- 2. Define the Specialized Sub-Agent (The "Tool") ---
# This agent's only job is to execute a search and return the raw, relevant information.
# It uses the built-in 'google_search' tool.
search_specialist_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="SearchSpecialist",
    description="A specialist agent that executes Google Search queries for current events and returns raw results with dates.",
    instruction="""
    You are a specialist in using Google Search to find current, trending information.
    When a user asks for news about an area, you MUST use the 'google_search' tool.
    Formulate the search query precisely, for example: 'top 10 news headlines for London'.
    Return the raw search results for the parent agent to process.
    Make sure to capture any date information available in the search results.
    """,
    tools=[google_search],
)

# --- 3. Wrap the Sub-Agent as an AgentTool ---
# This wrapper allows the Root Agent to treat the entire SearchSpecialist as a single function/tool.
search_tool = AgentTool(agent=search_specialist_agent)

# --- 4. Define the Root Agent (The "News Curator") ---
# The Root Agent is the orchestrator and the primary interface for the user.
# It reasons, delegates the search task, and synthesizes the final answer.
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="NewsCuratorAgent",
    description="A helpful assistant that finds the top 10 news headlines with dates for a specified city or country.",
    instruction=f"""
    You are a professional News Curator. Your goal is to find the top 10 most current and relevant news headlines 
    for the city or country provided by the user.

    Execution Steps:
    1. Identify the location from the user's query.
    2. Use the 'SearchSpecialist' tool to execute the Google Search query (e.g., 'top 10 news for [Location]').
    3. Synthesize the raw search results from the tool into a clear, concise, and numbered list of the top 10 headlines or brief summaries.
    4. For EACH headline, include the date of occurrence if available in the search results. Format: "[Date] - Headline text".
    5. If a date is not available for a specific news item, indicate it as "[Date unknown] - Headline text".
    6. You must only respond with the synthesized news report.
    7. If no location is provided, politely ask the user for one.
    """,
    # The Root Agent only has one tool: the AgentTool wrapper for the Sub-Agent
    tools=[search_tool],
)

# # --- 5. Runner Function (Optional for adk web) ---
# # This function provides a way to run and test the agent directly from the command line.
# def run_news_agent(query: str):
#     """Initializes a session with the root_agent and runs the user's query."""
    
#     # Simple check for API key
#     if not os.getenv("GEMINI_API_KEY"):
#         print("Error: GEMINI_API_KEY not found in .env file. Please add your key.")
#         sys.exit(1)
        
#     # Start a new session with the root_agent
#     session = Session(agent=root_agent)
    
#     print(f"👤 User Query: {query}\n")
#     print("🤖 News Curator Agent is thinking and searching...")
    
#     # Run the agent and get the response
#     # The LLM in the root_agent decides to call the search_tool (sub-agent)
#     response = session.run(query)
    
#     print("\n--- 📰 Final Top 5 News Report ---")
#     print(response.text)
#     print("----------------------------------")

# # --- 6. Main Execution Block (Optional for adk web) ---
# # This block ensures the script only runs the example query when executed directly 
# # (i.e., 'python agent.py'), but is ignored when imported by the ADK framework.
# if __name__ == "__main__":
#     # Example Query - Replace 'London' with any city or country
#     run_news_agent("What are the top 5 news stories in Berlin today?")

#     # Example of a query where the agent should ask for a location (optional test)
#     # run_news_agent("What's the latest breaking news?")

# nothing. just to trigger deployment.