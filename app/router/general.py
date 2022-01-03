from fastapi import APIRouter

from app.model.response import SuccessResponse
from ..dependencies import DATA
from ..model.general import GeneralResponse

router = APIRouter()


@router.get("/")
async def general_controller():
    daily_data = DATA["update"]["harian"]

    resp_obj = GeneralResponse(0, 0, 0, 0, 0, 0, 0, 0)
    for data in daily_data:
        resp_obj.total_deaths += data["jumlah_meninggal"]["value"]
        resp_obj.total_recovered += data["jumlah_sembuh"]["value"]
        resp_obj.total_positive += data["jumlah_positif"]["value"]
        resp_obj.total_active += data["jumlah_dirawat"]["value"]
        resp_obj.new_deaths += data["jumlah_meninggal_kum"]["value"]
        resp_obj.new_recovered += data["jumlah_sembuh_kum"]["value"]
        resp_obj.new_positive += data["jumlah_positif_kum"]["value"]
        resp_obj.new_active += data["jumlah_dirawat_kum"]["value"]

    return SuccessResponse(resp_obj)
