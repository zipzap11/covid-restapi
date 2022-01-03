from typing import Dict, List
from fastapi import APIRouter
from fastapi.params import Depends

from app.helper.validate import validate_empty_list, validate_empty_obj, validate_year
from app.model.response import SuccessResponse
from ..dependencies import fetch_data, DATA
from ..model.year import YearResponse

router = APIRouter()

# get the year of the first data
default_since = DATA[0]["key_as_string"][:4]
# get the year of the last data
default_upto = DATA[-1]["key_as_string"][:4]


@router.get("/yearly")
async def yearly_controller(
    data: List = Depends(fetch_data),
    since: str = default_since,
    upto: str = default_upto,
):
    validate_year(since)
    validate_year(upto)

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
async def yearly_year_controller(year: str, data: List = Depends(fetch_data)):
    validate_year(year)

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
