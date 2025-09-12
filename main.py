from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from controller import router
from dotenv import load_dotenv

app = FastAPI(
    title="Debate Bot API",
    description="API for a debate bot that defends positions",
    version="1.0.0"
)


app.include_router(router)

if __name__ == "__main__":

    load_dotenv()  
    port = int(os.getenv("PORT"))
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
    )