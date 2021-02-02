from fastapi import FastAPI
import uvicorn
from models.Model import SessionLocal 


import Routers 

app = FastAPI()

app.include_router(Routers.router)

if __name__ == "__main__":
    uvicorn.run(app=app)


