from typing import Dict
from fastapi import APIRouter
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


@router.get("/daily")
def daily_controller(since: str = default_since, upto: str = default_upto):

    year_since, month_since, day_since = separate_date(since, ".")
    year_upto, month_upto, day_upto = separate_date(upto, ".")

    resp_list = []
    data = DATA["update"]["harian"]

    for val in data:
        date = val["key_as_string"][:10]
        year, month, day = separate_date(date, "-")

        # validate date
        if year < year_since or year > year_upto:
            continue
        if (year == year_since and month < month_since) or (
            year == year_upto and month > month_upto
        ):
            continue
        if year == year_since and month == month_since and day < day_since:
            continue
        if year == year_upto and month == month_upto and day > day_upto:
            continue

        daily_data = new_day_resp(val)
        resp_list.append(daily_data)

    return resp_list
