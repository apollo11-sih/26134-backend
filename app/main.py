from fastapi import FastAPI

app = FastAPI(
    title="skillsync",
    description="Labour Market Intelligence Platform",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "message": "Backend is running!!"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }