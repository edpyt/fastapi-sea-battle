from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.api.di.providers.services import get_game_services
from src.domain.lobby.dto import GameDTO
from src.domain.lobby.usecases import GameServices
from src.infrastructure.db.models import Game

router = APIRouter()


@router.get(
    '/', response_description='Get all games lobbies'
)
async def get_games(
    game_services: GameServices = Depends(get_game_services)
) -> list[Game]:
    return await game_services.get_all_games()


@router.post('/create/', response_description='Create game lobby')
async def create_game(
    player_1_id: PydanticObjectId, 
    player_2_id: PydanticObjectId, 
    new_game: GameDTO,
    game_services: GameServices = Depends(get_game_services)
):
    print(player_1_id)
    print(player_2_id) 
    print(new_game)
    print('-'*100)
    # await game_services.create_game(new_game)
    return JSONResponse({'is_created': True}, status_code=200)