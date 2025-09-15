from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .properties import properties
from .controller import router

app = FastAPI(
    title="Debate Bot API",
    description="API for a debate bot that defends positions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000
    )