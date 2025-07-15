from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from scrapegraphai.graphs import SmartScraperGraph
from langchain_openai import ChatOpenAI
import asyncio

app = FastAPI()
mcp = FastApiMCP(app)
mcp.mount()

instance_config = {
    "model": "google/gemini-2.5-flash-preview-05-20",
    "openai_api_base": "https://openrouter.ai/api/v1",
    "api_key": "sk-or-v1-"
}

llm_model_instance = ChatOpenAI(**instance_config)

graph_config = {
    "llm": {
        "model_instance": llm_model_instance,
        "model_tokens": 5000
    },
    "verbose": True,
    "headless": True
}

class ScrapeRequest(BaseModel):
    url: str
    prompt: str

@app.post("/scrape")
async def scrape_website(request: ScrapeRequest):
    try:
        # Create the SmartScraperGraph instance
        smart_scraper_graph = SmartScraperGraph(
            prompt=request.prompt,
            source=request.url,
            config=graph_config
        )

        # Run the pipeline in a separate thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, smart_scraper_graph.run)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
