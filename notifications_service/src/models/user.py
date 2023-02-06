from base import BasePydanticModel


class UserModel(BasePydanticModel):
    username: str
    email: str
