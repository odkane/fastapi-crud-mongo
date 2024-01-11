import uvicorn
from fastapi import FastAPI

from server.routes.route import router

app = FastAPI()
app.include_router(router=router)


@app.get("/")
def welcome():
    return "Welcome to the test App!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
