from fastapi import FastAPI

from .router import general
from .dependencies import DATA

app = FastAPI()

app.include_router(general.router)


@app.get("/data")
def data():
    return DATA
