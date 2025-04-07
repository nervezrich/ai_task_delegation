from fastapi import FastAPI
import uvicorn
from api.endpoint import router

app = FastAPI()

# Include API routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Task Delegation AI is Running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
