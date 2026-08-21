from fastapi import FastAPI

app = FastAPI(
    title="Sentinel AI",
    description="AI-powered cybersecurity intelligence platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "status": "running",
        "project": "Sentinel AI",
        "version": "0.1.0"
    }