from db.models.models import User
from services.base_postgres_service import BaseService


class UserService(BaseService):
    _model = User


user_service: UserService = UserService()


def get_user_service() -> UserService:
    """Function for dependency injection"""

    return user_service
