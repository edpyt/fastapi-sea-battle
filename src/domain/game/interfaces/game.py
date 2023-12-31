from src.domain.common.usecases.base import BaseUseCase
from src.infrastructure.db.uow import UnitOfWork


class GameUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)
