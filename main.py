from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from ticketmaster import search_events
import uvicorn

app = FastAPI(title="Local Events Finder")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api/events")
async def get_events(
    location: str = Query(..., description="City name or zip code"),
    keyword: str = Query(None, description="Optional keyword filter"),
    radius: str = Query("25", description="Search radius in miles"),
):
    try:
        events = await search_events(location=location, keyword=keyword, radius=radius)
        return {"events": events, "count": len(events)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)