from app.api.models.room_model import RoomList
from app.services.requester import Requester
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

router = APIRouter()

# -----------------------------RECOMENDATIONS-----------------------------------#


@router.get(
    "",
    response_model=RoomList,
    status_code=HTTP_200_OK
)
async def get_recomended_rooms():
    rooms, _ = Requester.room_srv_fetch(
        method="GET", path="/recomendations", expected_statuses={HTTP_200_OK}
    )

    return rooms

# ------------------------------------------------------------------------------#
