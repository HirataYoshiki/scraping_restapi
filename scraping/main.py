from fastapi import FastAPI
import uvicorn
from models.Model import engine


import Routers 

app = FastAPI()

app.include_router(Routers.router)

@app.on_event("startup")
async def startup():
    engine.connect()

@app.on_event("shutdown")
async def shutdown():
    engine.disconnect()

if __name__ == "__main__":
    uvicorn.run(app=app)


