from models.base import BasePydanticModel


class UserModel(BasePydanticModel):
    username: str
    email: str
