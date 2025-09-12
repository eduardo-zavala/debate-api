from fastapi import FastAPI
import os

# Crear la app
app = FastAPI()

# Un solo endpoint - Hello World
@app.get("/")
def hello_world():
    return {"message": "Hello World from Render!"}

# Esto es necesario para que Render pueda ejecutar la app
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)