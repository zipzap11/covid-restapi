from typing import Dict
from fastapi import APIRouter

from app.helper.validate import validate_empty_list, validate_empty_obj, validate_year
from app.model.response import SuccessResponse
from ..dependencies import DATA
from ..model.year import YearResponse

router = APIRouter()

# get the year of the first data
default_since = DATA["update"]["harian"][0]["key_as_string"][:4]
# get the year of the last data
default_upto = DATA["update"]["harian"][-1]["key_as_string"][:4]


@router.get("/yearly")
async def yearly_controller(since: str = default_since, upto: str = default_upto):
    validate_year(since)
    validate_year(upto)

    data = DATA["update"]["harian"]
    resp_list = []

    yearly_data: Dict[int, YearResponse] = {}
    for val in data:
        year = int(val["key_as_string"][:4])

        if year < int(since) or year > int(upto):
            continue

        if year not in yearly_data.keys():
            yearly_data[year] = YearResponse(year, 0, 0, 0, 0)

        yearly_data[year].positive += val["jumlah_positif"]["value"]
        yearly_data[year].deaths += val["jumlah_meninggal"]["value"]
        yearly_data[year].recovered += val["jumlah_sembuh"]["value"]
        yearly_data[year].active += val["jumlah_dirawat"]["value"]

    for value in yearly_data.values():
        resp_list.append(value)

    validate_empty_list(resp_list)

    return SuccessResponse(resp_list)


@router.get("/yearly/{year}")
async def yearly_year_controller(year: str):
    validate_year(year)

    data = DATA["update"]["harian"]

    year_data = ""
    positive = 0
    deaths = 0
    recovered = 0
    active = 0
    for val in data:
        year_data = val["key_as_string"][:4]
        if year != year_data:
            continue

        positive += int(val["jumlah_positif"]["value"])
        deaths += int(val["jumlah_meninggal"]["value"])
        recovered += int(val["jumlah_sembuh"]["value"])
        active += int(val["jumlah_dirawat"]["value"])

    validate_empty_obj(year_data == "")

    resp_obj = YearResponse(year, positive, recovered, deaths, active)

    return SuccessResponse(resp_obj)
