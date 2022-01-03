from typing import Dict
from fastapi import APIRouter
from ..dependencies import DATA
from ..model.year import YearResponse

router = APIRouter()

# get the year of the first data
default_since = int(DATA["update"]["harian"][0]["key_as_string"][:4])
# get the year of the last data
default_upto = int(DATA["update"]["harian"][-1]["key_as_string"][:4])


@router.get("/yearly")
async def yearly_controller(since: int = default_since, upto: int = default_upto):
    data = DATA["update"]["harian"]
    resp_list = []

    yearly_data: Dict[int, YearResponse] = {}
    for val in data:
        year = int(val["key_as_string"][:4])

        if year < since or year > upto:
            continue

        if year not in yearly_data.keys():
            yearly_data[year] = YearResponse(year, 0, 0, 0, 0)

        yearly_data[year].positive += val["jumlah_positif"]["value"]
        yearly_data[year].deaths += val["jumlah_meninggal"]["value"]
        yearly_data[year].recovered += val["jumlah_sembuh"]["value"]
        yearly_data[year].active += val["jumlah_dirawat"]["value"]

    for value in yearly_data.values():
        resp_list.append(value)

    return resp_list


@router.get("/yearly/{year}")
async def specific_year_controller(year: str):
    data = DATA["update"]["harian"]
    resp_obj = YearResponse(year, 0, 0, 0, 0)

    for val in data:
        if not (year == val["key_as_string"][:4]):
            continue

        resp_obj.positive += int(val["jumlah_positif"]["value"])
        resp_obj.deaths += int(val["jumlah_meninggal"]["value"])
        resp_obj.recovered += int(val["jumlah_sembuh"]["value"])
        resp_obj.active += int(val["jumlah_dirawat"]["value"])

    return resp_obj
