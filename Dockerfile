FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable for port
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run ADK web server with proper binding
CMD adk web --agent news_agent.agent:root_agent --host 0.0.0.0 --port $PORT