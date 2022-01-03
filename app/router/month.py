from typing import Dict, Optional
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.helper.validate import (
    validate_empty_list,
    validate_month,
    validate_moth_query,
    validate_same_year,
    validate_year,
)

from ..helper.helper import from_dictval_to_list
from ..dependencies import DATA
from ..model.month import MonthResponse

router = APIRouter()

# get the year.month code of the first data
key = DATA["update"]["harian"][0]["key_as_string"]
default_since = key[:4] + "." + key[5:7]
# get the year.month code of the last data
key = DATA["update"]["harian"][-1]["key_as_string"]
default_upto = key[:4] + "." + key[5:7]


# get moth code (year*moth), separate year and month, and return it as int
def split_moth_code(moth, separator):
    tmp = moth.split(separator)
    year = tmp[0]
    month = tmp[1]

    validate_year(year)
    validate_month(month)

    if tmp[1][0] == "0":
        month = tmp[1][1]
    else:
        month = tmp[1]
    return int(year), int(month)


@router.get("/monthly")
def monthly_controller(since: str = default_since, upto: str = default_upto):
    data = DATA["update"]["harian"]

    validate_moth_query(since)
    validate_moth_query(upto)

    # get year-month code
    year_since, month_since = split_moth_code(since, ".")
    year_upto, month_upto = split_moth_code(upto, ".")

    monthly_data: Dict[str, MonthResponse] = {}
    for val in data:
        moth: str = val["key_as_string"][:7]
        [year, month] = split_moth_code(moth, "-")

        # filter based on query param
        if year < year_since or year > year_upto:
            continue
        if year == year_since and month < month_since:
            continue
        if year == year_upto and month > month_upto:
            continue

        if moth not in monthly_data.keys():
            monthly_data[moth] = MonthResponse(moth, 0, 0, 0, 0)

        monthly_data[moth].positive += val["jumlah_positif"]["value"]
        monthly_data[moth].deaths += val["jumlah_meninggal"]["value"]
        monthly_data[moth].recovered += val["jumlah_sembuh"]["value"]
        monthly_data[moth].active += val["jumlah_dirawat"]["value"]

    list_resp = from_dictval_to_list(monthly_data)
    validate_empty_list(list_resp)

    return list_resp


@router.get("/monthly/{year}")
def monthly_year_controller(
    year: str, since: Optional[str] = None, upto: Optional[str] = None
):
    validate_year(year)

    if not since:
        since = str(year) + ".01"
    if not upto:
        upto = str(year) + ".12"

    validate_moth_query(since)
    validate_moth_query(upto)

    year_since, month_since = split_moth_code(since, ".")
    year_upto, month_upto = split_moth_code(upto, ".")

    validate_same_year(int(year), year_since, year_upto)

    data = DATA["update"]["harian"]

    monthly_data: Dict[int, MonthResponse] = {}
    for val in data:
        moth = val["key_as_string"][:7]

        data_year, data_month = split_moth_code(moth, "-")

        if int(year) != data_year:
            continue

        if data_month < month_since or data_month > month_upto:
            continue

        if data_month not in monthly_data.keys():
            monthly_data[data_month] = MonthResponse(moth, 0, 0, 0, 0)

        monthly_data[data_month].positive += val["jumlah_positif"]["value"]
        monthly_data[data_month].deaths += val["jumlah_meninggal"]["value"]
        monthly_data[data_month].recovered += val["jumlah_sembuh"]["value"]
        monthly_data[data_month].active += val["jumlah_dirawat"]["value"]

    list_resp = from_dictval_to_list(monthly_data)
    validate_empty_list(list_resp)

    return list_resp


@router.get("/monthly/{year}/{month}")
def montly_year_month_controller(year: str, month: str):
    validate_year(year)
    validate_month(month)

    data = DATA["update"]["harian"]

    moth_resp = year + "-" + month

    for val in data:
        moth = val["key_as_string"][:7]

        if moth != moth_resp:
            continue

        return new_month_resp(val)

    raise HTTPException(status_code=404, detail="not found")


def new_month_resp(source: Dict):
    moth = source["key_as_string"][:7]
    positive = source["jumlah_positif"]["value"]
    deaths = source["jumlah_meninggal"]["value"]
    recovered = source["jumlah_sembuh"]["value"]
    active = source["jumlah_dirawat"]["value"]

    return MonthResponse(moth, positive, recovered, deaths, active)
