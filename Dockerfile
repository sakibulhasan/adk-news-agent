FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run ADK web server
CMD ["adk", "web", "--agent", "news_agent.agent:root_agent", "--port", "8080"]