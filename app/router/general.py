from typing import List
from fastapi import APIRouter
from fastapi.params import Depends

from app.model.response import SuccessResponse
from ..dependencies import DATA, fetch_data
from ..model.general import GeneralResponse

router = APIRouter()


@router.get("/")
async def general_controller(data: List = Depends(fetch_data)):
    resp_obj = GeneralResponse(0, 0, 0, 0, 0, 0, 0, 0)

    for val in data:
        resp_obj.total_deaths += val["jumlah_meninggal"]["value"]
        resp_obj.total_recovered += val["jumlah_sembuh"]["value"]
        resp_obj.total_positive += val["jumlah_positif"]["value"]
        resp_obj.total_active += val["jumlah_dirawat"]["value"]
        resp_obj.new_deaths += val["jumlah_meninggal_kum"]["value"]
        resp_obj.new_recovered += val["jumlah_sembuh_kum"]["value"]
        resp_obj.new_positive += val["jumlah_positif_kum"]["value"]
        resp_obj.new_active += val["jumlah_dirawat_kum"]["value"]

    return SuccessResponse(resp_obj)
