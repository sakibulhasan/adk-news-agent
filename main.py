from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from news_agent.agent import root_agent
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(
    title="News Agent API",
    description="A multi-agent news retrieval system built with Google's ADK",
    version="1.0.0"
)

class NewsRequest(BaseModel):
    query: str

class NewsResponse(BaseModel):
    response: str
    status: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "healthy",
        "service": "News Agent API",
        "message": "Send POST requests to /chat with your news queries"
    }

@app.get("/health")
async def health():
    """Health check endpoint for GCP load balancer"""
    return {"status": "ok"}

@app.post("/chat", response_model=NewsResponse)
async def chat(request: NewsRequest):
    """Chat with the news agent"""
    try:
        # Validate API key
        if not os.getenv("GOOGLE_API_KEY"):
            raise HTTPException(
                status_code=500, 
                detail="API key not configured"
            )
        
        # Use the agent's send_message method directly
        response = root_agent.send_message(request.query)
        
        return NewsResponse(
            response=response.text if hasattr(response, 'text') else str(response),
            status="success"
        )
        
    except Exception as e:
        import traceback
        error_detail = f"Error processing request: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)