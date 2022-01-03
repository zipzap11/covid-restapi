from typing import Dict, Optional
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ..dependencies import DATA
from ..model.date import DayResponse

router = APIRouter()

# get first date
key = DATA["update"]["harian"][0]["key_as_string"]
default_since = key[:4] + "." + key[5:7] + "." + key[8:10]
# get last date
key = DATA["update"]["harian"][-1]["key_as_string"]
default_upto = key[:4] + "." + key[5:7] + "." + key[8:10]


def separate_date(date: str, separator: str):
    arr_date = date.split(separator)
    year = arr_date[0]
    month = arr_date[1]
    day = arr_date[2]

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


def validate_date(year: int, month: int, day: int, since: Dict, upto: Dict):
    if year < since["year"] or year > upto["year"]:
        return False
    if (year == since["year"] and month < since["month"]) or (
        year == upto["year"] and month > upto["month"]
    ):
        return False
    if year == since["year"] and month == since["month"] and day < since["day"]:
        return False
    if year == upto["year"] and month == upto["month"] and day > upto["day"]:
        return False

    return True


@router.get("/daily")
async def daily_controller(since: str = default_since, upto: str = default_upto):
    year_since, month_since, day_since = separate_date(since, ".")
    year_upto, month_upto, day_upto = separate_date(upto, ".")

    since_dict = {"year": year_since, "month": month_since, "day": day_since}
    upto_dict = {"year": year_upto, "month": month_upto, "day": day_upto}

    resp_list = []
    data = DATA["update"]["harian"]

    for val in data:
        date = val["key_as_string"][:10]
        year, month, day = separate_date(date, "-")

        if not validate_date(year, month, day, since_dict, upto_dict):
            continue

        daily_data = new_day_resp(val)
        resp_list.append(daily_data)

    return resp_list


@router.get("/daily/{year}")
async def daily_year_controller(
    year: int, since: Optional[str] = None, upto: Optional[str] = None
):
    if not since:
        since = str(year) + ".01.01"
    if not upto:
        upto = str(year) + ".12.31"

    month_since, day_since = separate_date(since, ".")[1:]
    month_upto, day_upto = separate_date(upto, ".")[1:]

    since_dict = {"year": year, "month": month_since, "day": day_since}
    upto_dict = {"year": year, "month": month_upto, "day": day_upto}

    data = DATA["update"]["harian"]
    resp_list = []

    for val in data:
        date = val["key_as_string"][:10]
        year_date, month_date, day_date = separate_date(date, "-")

        if not validate_date(year_date, month_date, day_date, since_dict, upto_dict):
            continue

        daily_data = new_day_resp(val)
        resp_list.append(daily_data)

    return resp_list


@router.get("/daily/{year}/{month}")
async def daily_year_month_controller(
    year: int, month: int, since: Optional[str] = None, upto: Optional[str] = None
):
    if not since:
        since = str(year) + "." + str(month) + ".01"
    if not upto:
        upto = str(year) + "." + str(month) + ".31"

    day_since = separate_date(since, ".")[2]
    day_upto = separate_date(upto, ".")[2]

    since_dict = {"year": year, "month": month, "day": day_since}
    upto_dict = {"year": year, "month": month, "day": day_upto}

    data = DATA["update"]["harian"]
    resp_list = []

    for val in data:
        date = val["key_as_string"][:10]
        year_date, month_date, day_date = separate_date(date, "-")

        if not validate_date(year_date, month_date, day_date, since_dict, upto_dict):
            continue

        daily_data = new_day_resp(val)
        resp_list.append(daily_data)

    return resp_list


@router.get("/daily/{year}/{month}/{day}")
def daily_year_month_day_controller(year: str, month: str, day: str):
    data = DATA["update"]["harian"]

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

        return new_day_resp(val)

    raise HTTPException(status_code=404, detail="not found")
