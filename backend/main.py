from fastapi import FastAPI
import uvicorn
from api.endpoint import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (React) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL (frontend running on port 3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.post("/")
def root():
    return {"message": "Task Delegation AI is Running"}

if __name__ == "__main__":
    # Run the FastAPI app on localhost with port 8008
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True)
