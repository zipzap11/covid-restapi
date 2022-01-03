from fastapi import FastAPI

from app.router import day


from .router import general, year, month
from .dependencies import DATA

app = FastAPI()

app.include_router(general.router)
app.include_router(year.router)
app.include_router(month.router)
app.include_router(day.router)
