# News Agent - ADK Multi-Agent System

A multi-agent news retrieval system built with Google's Agent Development Kit (ADK) that fetches the top 10 current news headlines with dates for any specified city or country.

## Features

- 🔍 **Smart Search**: Uses Google Search to find current news
- 📰 **Top 10 Headlines**: Retrieves the most relevant and recent news stories
- 📅 **Date Information**: Includes occurrence dates for each news item
- 🤖 **Multi-Agent Architecture**: Specialized sub-agent for search execution and root agent for synthesis
- 🌍 **Location-Based**: Supports any city or country

## Architecture

The system uses a two-tier agent architecture:

1. **SearchSpecialist** (Sub-Agent): Executes Google search queries and returns raw results
2. **NewsCuratorAgent** (Root Agent): Orchestrates the process and synthesizes results into a formatted list

## Prerequisites

- Python 3.8 or higher
- Google ADK installed
- Gemini API key

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/sakibulhasan/code/adk/adk-news-agent
   ```

2. **Install required dependencies**:
   ```bash
   pip install google-adk python-dotenv
   ```

3. **Create a `.env` file** in the project root:
   ```bash
   touch .env
   ```

4. **Add your Gemini API key** to the `.env` file:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=0
   GOOGLE_API_KEY=your_api_key_here
   ```

   > To get a Gemini API key, visit: https://makersuite.google.com/app/apikey

## Running Locally

### Option 1: Using ADK Web Interface

1. **Start the ADK web server**:
   ```bash
   adk web news_agent.agent:root_agent
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

3. **Interact with the agent** by typing queries like:
   - "What are the top 10 news stories in London today?"
   - "Give me the latest news from Berlin"
   - "What's happening in New York?"

### Option 2: Command Line (Uncomment the test code)

If you want to test directly from the command line:

1. **Uncomment lines 62-100** in `news_agent/agent.py` (the `run_news_agent` function and `if __name__ == "__main__"` block)

2. **Run the script**:
   ```bash
   python news_agent/agent.py
   ```

3. **Modify the query** in the script to test different locations

## Project Structure

```
adk-news-agent/
├── news_agent/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Main agent implementation
│   └── __pycache__/         # Python cache files
├── .env                     # Environment variables (create this)
└── README.md                # This file
```

## Usage Examples

**Query Format:**
```
What are the top 10 news stories in [LOCATION] today?
```

**Example Queries:**
- "What are the top 10 news stories in Tokyo?"
- "Give me the latest news from Paris"
- "What's happening in Australia?"
- "Top news in San Francisco"

**Expected Output Format:**
```
1. [Nov 18, 2025] - Headline text here...
2. [Nov 17, 2025] - Another headline...
3. [Date unknown] - Headline without date...
...
10. [Nov 18, 2025] - Final headline...
```

## Configuration

The agent uses the following models and settings:

- **Model**: `gemini-2.5-flash`
- **Number of Headlines**: 10 (configurable in agent instructions)
- **Search Tool**: Built-in `google_search` from ADK

## Troubleshooting

**Issue**: "GEMINI_API_KEY not found"
- **Solution**: Ensure your `.env` file exists and contains the API key

**Issue**: "Module not found" error
- **Solution**: Install dependencies: `pip install google-adk python-dotenv`

**Issue**: Agent doesn't return dates
- **Solution**: The agent returns dates when available in search results. Some news sources may not provide dates.

**Issue**: Port 8000 already in use
- **Solution**: Stop other services on port 8000 or specify a different port:
  ```bash
  adk web news_agent.agent:root_agent --port 8080
  ```

## Development

To modify the agent behavior:

1. **Change number of headlines**: Edit the instructions in `root_agent` (line 47)
2. **Modify search behavior**: Update `search_specialist_agent` instructions (line 24)
3. **Add error handling**: Implement try-catch blocks in the uncommented runner function
4. **Add caching**: Implement a caching layer for recent queries

## License

This project is for educational and development purposes.

## Support

For ADK documentation and support, visit:
- [Google ADK Documentation](https://ai.google.dev/adk)
- [Gemini API Documentation](https://ai.google.dev/gemini-api)
