from typing import Dict, List
from fastapi.exceptions import HTTPException


def validate_year(year: str):
    if not year.isdecimal():
        raise HTTPException(status_code=400, detail="invalid year")

    length = len(year)
    year_int = int(year)
    if length != 4 or year[0] == "0" or year_int <= 0 or year_int > 2022:
        raise HTTPException(status_code=400, detail="invalid year")


def validate_month(month: str):
    if not month.isdecimal():
        raise HTTPException(status_code=400, detail="invalid month")

    length = len(month)
    month_int = 0
    if str(month)[0] == "0":
        month_int = int(month[1:])
    else:
        month_int = int(month)

    if length != 2 or month_int <= 0 or month_int > 12:
        raise HTTPException(status_code=400, detail="invalid month")


def validate_day(day: str):
    if not day.isdecimal():
        raise HTTPException(status_code=400, detail="invalid day")

    length = len(day)
    day_int = int(day)

    if length != 2 or day_int < 0 or day_int > 31:
        raise HTTPException(status_code=400, detail="invalid day")


def validate_date_range(year: int, month: int, day: int, since: Dict, upto: Dict):
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


def validate_same_year(year, year_since, year_upto):
    if year_since != year or year_upto != year:
        raise HTTPException(
            status_code=400,
            detail="invalid query params on year, year has to be the same",
        )


def validate_same_month(month, month_since, month_upto):
    if month_since != month or month_upto != month:
        raise HTTPException(
            status_code=400,
            detail="invalid query params on month, month value has to be the same",
        )


def validate_empty_list(list: List):
    if len(list) == 0:
        raise HTTPException(status_code=404, detail="not found")


def validate_empty_obj(flag: bool):
    if flag:
        raise HTTPException(status_code=404, detail="not found")


def validate_date_query(date: str):
    if (
        len(date) != 10
        or date[4] != "."
        or date[7] != "."
        or not date[:4].isnumeric()
        or not date[5:7].isnumeric()
        or not date[8:].isnumeric()
    ):
        raise HTTPException(status_code=400, detail="invalid query params")


def validate_moth_query(moth: str):
    if (
        len(moth) != 7
        or moth[4] != "."
        or not moth[:4].isnumeric()
        or not moth[5:7].isnumeric()
    ):
        raise HTTPException(status_code=400, detail="invalid query params")
