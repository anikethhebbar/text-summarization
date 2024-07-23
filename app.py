from fastapi import FastAPI
from routes.summarization_routes import router as summarization_router

app = FastAPI()

# Include the routes for the summarization API in the FastAPI app
app.include_router(summarization_router)

@app.get("/")
async def root():
    return {"message": "Welcome to DS-SUMMARIZATION API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)