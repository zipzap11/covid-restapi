from typing import Dict, List, Optional
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends

from app.helper.validate import (
    validate_date_query,
    validate_date_range,
    validate_day,
    validate_empty_list,
    validate_month,
    validate_same_month,
    validate_same_year,
    validate_year,
)
from app.model.response import SuccessResponse
from ..dependencies import DATA, fetch_data
from ..model.date import DayResponse

router = APIRouter()


# get first date
key = DATA[0]["key_as_string"]
default_since = key[:4] + "." + key[5:7] + "." + key[8:10]
# get last date
key = DATA[-1]["key_as_string"]
default_upto = key[:4] + "." + key[5:7] + "." + key[8:10]


@router.get("/daily")
async def daily_controller(since: str = default_since, upto: str = default_upto, data: List = Depends(fetch_data)):
    validate_date_query(since)
    validate_date_query(upto)

    year_since, month_since, day_since = separate_date(since, ".")
    year_upto, month_upto, day_upto = separate_date(upto, ".")

    since_dict = {"year": year_since, "month": month_since, "day": day_since}
    upto_dict = {"year": year_upto, "month": month_upto, "day": day_upto}

    resp_list = []

    for val in data:
        date = val["key_as_string"][:10]
        year, month, day = separate_date(date, "-")

        if not validate_date_range(year, month, day, since_dict, upto_dict):
            continue

        daily_data = new_day_resp(val)
        resp_list.append(daily_data)

    validate_empty_list(resp_list)

    return SuccessResponse(resp_list)


@router.get("/daily/{year}")
async def daily_year_controller(
    year: str, since: Optional[str] = None, upto: Optional[str] = None, data: List = Depends(fetch_data)
):
    validate_year(year)

    if not since:
        since = year + ".01.01"
    if not upto:
        upto = year + ".12.31"

    validate_date_query(since)
    validate_date_query(upto)

    year_since, month_since, day_since = separate_date(since, ".")
    year_upto, month_upto, day_upto = separate_date(upto, ".")

    validate_same_year(int(year), year_since, year_upto)

    since_dict = {"year": int(year), "month": month_since, "day": day_since}
    upto_dict = {"year": int(year), "month": month_upto, "day": day_upto}

    resp_list = []

    for val in data:
        date = val["key_as_string"][:10]
        year_date, month_date, day_date = separate_date(date, "-")

        if not validate_date_range(
            year_date, month_date, day_date, since_dict, upto_dict
        ):
            continue

        daily_data = new_day_resp(val)
        resp_list.append(daily_data)

    validate_empty_list(resp_list)

    return SuccessResponse(resp_list)


@router.get("/daily/{year}/{month}")
async def daily_year_month_controller(
    year: str, month: str, since: Optional[str] = None, upto: Optional[str] = None, data: List = Depends(fetch_data)
):
    validate_year(str(year))
    validate_month(str(month))

    if not since:
        since = str(year) + "." + str(month) + ".01"
    if not upto:
        upto = str(year) + "." + str(month) + ".31"

    validate_date_query(since)
    validate_date_query(upto)

    year_since, month_since, day_since = separate_date(since, ".")
    year_upto, month_upto, day_upto = separate_date(upto, ".")

    validate_same_year(int(year), year_since, year_upto)
    validate_same_month(int(month), month_since, month_upto)

    since_dict = {"year": int(year), "month": int(month), "day": day_since}
    upto_dict = {"year": int(year), "month": int(month), "day": day_upto}

    resp_list = []

    for val in data:
        date = val["key_as_string"][:10]
        year_date, month_date, day_date = separate_date(date, "-")

        if not validate_date_range(
            year_date, month_date, day_date, since_dict, upto_dict
        ):
            continue

        daily_data = new_day_resp(val)
        resp_list.append(daily_data)

    validate_empty_list(resp_list)

    return SuccessResponse(resp_list)


@router.get("/daily/{year}/{month}/{day}")
async def daily_year_month_day_controller(year: str, month: str, day: str, data: List = Depends(fetch_data)):
    # parameter validation
    validate_year(year)
    validate_month(month)
    validate_day(day)

    # handling zero as the first number
    if day[0] == "0":
        day = day[1]
    if month[0] == "0":
        month = month[1]

    for val in data:
        date = val["key_as_string"][:10]
        year_date, month_date, day_date = separate_date(date, "-")

        if year_date != int(year) or month_date != int(month) or day_date != int(day):
            continue

        resp = new_day_resp(val)
        return SuccessResponse(resp)

    raise HTTPException(
        status_code=404,
        detail="not found",
    )


def separate_date(date: str, separator: str):
    arr_date = date.split(separator)
    year = arr_date[0]
    month = arr_date[1]
    day = arr_date[2]

    validate_year(year)
    validate_month(month)
    validate_day(day)

    if month[0] == "0":
        month = month[1]
    if day[0] == "0":
        day = day[1]

    return int(year), int(month), int(day)


def new_day_resp(source: Dict):
    date = source["key_as_string"][:10]
    positive = source["jumlah_positif"]["value"]
    deaths = source["jumlah_meninggal"]["value"]
    recovered = source["jumlah_sembuh"]["value"]
    active = source["jumlah_dirawat"]["value"]

    return DayResponse(date, positive, recovered, deaths, active)
